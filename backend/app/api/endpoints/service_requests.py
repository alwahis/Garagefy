from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from typing import Dict, Any, List
import logging
import os
import time
from datetime import datetime
from ...services.baserow_service import baserow_service as airtable_service
from ...services.fix_it_service import fix_it_service

router = APIRouter()
logger = logging.getLogger(__name__)

async def _process_service_request(
    name: str,
    email: str,
    phone: str,
    car_brand: str,
    vin: str,
    license_plate: str,
    notes: str,
    images: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Process service request and return result"""
    try:
        logger.info(f"Starting to process service request for: {name} <{email}>")
        logger.info(f"Request includes {len(images)} images")
        
        # Upload images to Cloudinary
        image_urls = []
        for img in images:
            try:
                if not isinstance(img, dict) or 'content' not in img:
                    logger.warning(f"Skipping invalid image data: {img}")
                    continue
                
                # Log image info (without content)
                logger.info(f"Uploading image to Cloudinary: {img.get('filename', 'unnamed')}, "
                           f"size: {len(img['content']) if img.get('content') else 0} bytes")
                
                # Upload to Cloudinary
                url = airtable_service._upload_file_to_cloudinary(
                    img['content'],
                    img.get('filename', f"image_{int(time.time())}.jpg")
                )
                
                if url:
                    image_urls.append({'url': url})
                    logger.info(f"Successfully uploaded image to Cloudinary: {url}")
                else:
                    logger.error(f"Failed to upload image to Cloudinary")
                
            except Exception as e:
                logger.error(f"Error uploading image to Cloudinary: {str(e)}", exc_info=True)
                continue
        
        logger.info(f"Uploaded {len(image_urls)} images to Cloudinary")
        
        # Process the form data and create the service request
        try:
            # Use the correct method to create a customer record in Baserow
            result = airtable_service.create_customer({
                'Name': name,
                'Email': email,
                'phone': phone,
                'car_brand': car_brand,
                'VIN': vin,
                'Plate Number': license_plate,
                'Note': notes,
                'Image': image_urls if image_urls else None
            })

            if not result or 'success' not in result:
                error_msg = "Invalid response from Baserow service"
                logger.error(error_msg)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=error_msg
                )

            if not result['success']:
                error_msg = result.get('error', 'Unknown error')
                logger.error(f"Failed to create service request: {error_msg}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to create service request: {error_msg}"
                )

            logger.info(f"Successfully processed service request for {email}")
            
            # Return result with image URLs
            return {
                'success': True,
                'record_id': result.get('record_id'),
                'image_urls': [img['url'] for img in image_urls],
                'error': None
            }
            
        except HTTPException:
            raise
        except Exception as e:
            error_msg = f"Error creating service request: {str(e)}"
            logger.exception(error_msg)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_msg
            )
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Unexpected error processing service request: {str(e)}"
        logger.exception(error_msg)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_msg
        )

def _send_notifications(
    request_id: str,
    car_brand: str,
    vin: str,
    license_plate: str,
    notes: str,
    image_urls: List[str]
):
    """Send quote request notifications to all garages in Fix it table.
    
    This function sends emails to garages WITHOUT customer PII (name, email, phone).
    Only includes request ID, car brand, VIN, damage notes, and image links.
    
    NOTE: This is a synchronous wrapper for the async email sending function
    to work properly with FastAPI BackgroundTasks.
    """
    import asyncio
    
    logger.info(f"⚡ BACKGROUND TASK STARTED - Preparing to send quote requests for request ID: {request_id}")
    
    try:
        logger.info(f"📧 Sending quote requests to garages for VIN: {vin}")
        
        # Create a new event loop for this background task
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                fix_it_service.send_quote_requests(
                    request_id=request_id,
                    car_brand=car_brand,
                    vin=vin,
                    license_plate=license_plate,
                    damage_notes=notes,
                    image_urls=image_urls
                )
            )
            
            if result.get('success'):
                logger.info(f"✅ BACKGROUND TASK SUCCESS - Sent quote requests to {result.get('garages_contacted', 0)} garages")
            else:
                logger.error(f"❌ BACKGROUND TASK FAILED - Failed to send quote requests: {result.get('error', 'Unknown error')}")
        finally:
            loop.close()
        
    except Exception as e:
        error_msg = f"❌ BACKGROUND TASK ERROR - Error sending quote requests to garages: {str(e)}"
        logger.error(error_msg, exc_info=True)
        # Don't re-raise as this is a background task

# Dictionary to store in-flight requests with timestamps (in production, use Redis or similar)
_in_flight_requests = {}

# Store processed request IDs with timestamps to prevent duplicates
_processed_request_ids = {}

# Timeout for in-flight requests (in seconds)
_IN_FLIGHT_TIMEOUT = 300  # 5 minutes

# Cleanup interval (in seconds)
_CLEANUP_INTERVAL = 3600  # 1 hour
_last_cleanup = 0

def _cleanup_old_requests():
    global _last_cleanup
    current_time = time.time()
    if current_time - _last_cleanup > _CLEANUP_INTERVAL:
        _last_cleanup = current_time
        logger.info("Cleaning up old requests")
        for request_key, (timestamp, _) in list(_in_flight_requests.items()):
            if current_time - timestamp > _IN_FLIGHT_TIMEOUT:
                logger.info(f"Removing expired request: {request_key}")
                _in_flight_requests.pop(request_key, None)
        for request_id, timestamp in list(_processed_request_ids.items()):
            if current_time - timestamp > _IN_FLIGHT_TIMEOUT:
                logger.info(f"Removing expired request ID: {request_id}")
                _processed_request_ids.pop(request_id, None)

def _generate_request_key(name: str, email: str, phone: str, vin: str, notes: str) -> str:
    """Generate a unique key for deduplication"""
    import hashlib
    request_str = f"{name}:{email}:{phone}:{vin}:{notes}"
    return hashlib.md5(request_str.encode()).hexdigest()

@router.post("/service-requests", response_model=Dict[str, Any])
async def create_service_request(
    background_tasks: BackgroundTasks,
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    carBrand: str = Form(...),
    vin: str = Form(...),
    licensePlate: str = Form(""),
    notes: str = Form(""),
    requestId: str = Form(""),
    images: List[UploadFile] = File([])
) -> Dict[str, Any]:
    logger.info(f"Received service request - Request ID: {requestId}")
    logger.info(f"Request headers: {dict(request.headers)}")
    
    try:
        current_time = time.time()
        logger.info(f"Processing request at timestamp: {current_time}")
        
        # Log basic request info
        logger.info(f"Request details - Name: {name}, Email: {email}, Phone: {phone}")
        logger.info(f"Request includes {len(images)} images")
        
        # Log form data (excluding sensitive info)
        form_data = await request.form()
        logger.info(f"Form data keys: {list(form_data.keys())}")
        
        # Log files info
        for i, img in enumerate(images):
            logger.info(f"Image {i+1}: {img.filename}, {img.content_type}, {img.size} bytes")
        
        # Run cleanup of old requests if needed
        _cleanup_old_requests()
        
        # Log CORS headers
        logger.info(f"Origin header: {request.headers.get('origin')}")
        logger.info(f"Access-Control-Request-Method: {request.headers.get('access-control-request-method')}")
        logger.info(f"Access-Control-Request-Headers: {request.headers.get('access-control-request-headers')}")
        
        # Check for duplicate request ID or similar recent request
        request_key = _generate_request_key(name, email, phone, vin, notes)
        
        # Check if we have a recent duplicate request
        if request_key in _in_flight_requests:
            timestamp, request_id = _in_flight_requests[request_key]
            if current_time - timestamp < _IN_FLIGHT_TIMEOUT:
                logger.warning(f"Duplicate request detected (key: {request_key[:8]}...), last processed {current_time - timestamp:.2f}s ago")
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={"detail": "A similar request was recently processed. Please wait before trying again."}
                )
            else:
                # Remove expired request
                _in_flight_requests.pop(request_key, None)
        
        # Also check the requestId if provided
        if requestId and requestId in _processed_request_ids:
            timestamp = _processed_request_ids[requestId]
            if current_time - timestamp < _IN_FLIGHT_TIMEOUT:
                logger.warning(f"Duplicate request ID detected: {requestId}")
                return JSONResponse(
                    status_code=status.HTTP_409_CONFLICT,
                    content={"detail": "This request has already been processed"}
                )
            else:
                # Remove expired request ID
                _processed_request_ids.pop(requestId, None)
                
        # Mark this request as in-flight using both the key and requestId
        _in_flight_requests[request_key] = (current_time, requestId or str(current_time))
        
        # Add request to in-flight requests
        _processed_request_ids[requestId or str(current_time)] = current_time
        
        # Process images if any
        image_data = []
        for image in images:
            try:
                # Ensure we're at the start of the file
                await image.seek(0)
                # Read the file content
                contents = await image.read()
                
                logger.info(f"Processing image: {image.filename}, size: {len(contents)} bytes, type: {image.content_type}")
                
                # Create a dictionary with file info and content
                file_info = {
                    "filename": image.filename or f"image_{int(time.time())}.jpg",
                    "content": contents,  # Actual binary content
                    "content_type": image.content_type or "application/octet-stream"
                }
                
                # Log file info (without content)
                logger.info(f"Added file to upload: {file_info['filename']} ({len(contents)} bytes, {file_info['content_type']})")
                
                image_data.append(file_info)
                
            except Exception as e:
                logger.error(f"Error processing image {getattr(image, 'filename', 'unknown')}: {str(e)}", exc_info=True)
                continue
        
        try:
            # Process the service request
            logger.info(f"🔵 DEBUG: About to call _process_service_request with {len(image_data)} images")
            result = await _process_service_request(
                name=name,
                email=email,
                phone=phone,
                car_brand=carBrand,
                vin=vin,
                license_plate=licensePlate,
                notes=notes,
                images=image_data
            )
            
            logger.info(f"🔵 DEBUG: _process_service_request returned: {result}")
            
            # Get the image URLs from the result
            image_urls = result.get('image_urls', [])
            
            logger.info(f"🔵 DEBUG: Extracted {len(image_urls)} image URLs")
            
            # Send quote requests to garages in BACKGROUND TASK
            # This prevents timeout when sending to 50+ garages
            logger.info(f"📧 Scheduling background task to send quote requests for VIN: {vin}")
            background_tasks.add_task(
                _send_notifications,
                request_id=requestId,
                car_brand=carBrand,
                vin=vin,
                license_plate=licensePlate,
                notes=notes,
                image_urls=image_urls
            )
            logger.info(f"✅ Background task scheduled - API will respond immediately")
            
            # Log success
            logger.info(f"Successfully processed request from {email}")
            logger.info(f"🔵 DEBUG: About to return result: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error in service request processing: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error processing service request: {str(e)}"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error in create_service_request")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your request: {str(e)}"
        )
