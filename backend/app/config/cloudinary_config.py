import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def configure_cloudinary():
    """Configure Cloudinary with credentials from environment variables"""
    cloudinary.config(
        cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
        api_key=os.getenv('CLOUDINARY_API_KEY'),
        api_secret=os.getenv('CLOUDINARY_API_SECRET'),
        secure=True
    )
    print("✅ Cloudinary configured successfully!")

def upload_file(file_content, public_id=None, folder="garagefy"):
    """
    Upload a file to Cloudinary
    
    Args:
        file_content: File content as bytes
        public_id: Optional public ID for the file
        folder: Folder to store the file in
        
    Returns:
        dict: Upload result from Cloudinary
    """
    try:
        # Configure Cloudinary
        configure_cloudinary()
        
        print(f"📤 Uploading file to Cloudinary folder: {folder}")
        
        # Upload the file
        upload_result = cloudinary.uploader.upload(
            file_content,
            public_id=public_id,
            folder=folder,
            resource_type="auto",
            chunk_size=6000000,  # 6MB chunks for large files
            timeout=30  # 30 second timeout
        )
        
        print(f"✅ File uploaded successfully: {upload_result.get('secure_url')}")
        
        return {
            'success': True,
            'url': upload_result.get('secure_url'),
            'public_id': upload_result.get('public_id'),
            'format': upload_result.get('format'),
            'bytes': upload_result.get('bytes')
        }
        
    except Exception as e:
        print(f"❌ Error uploading to Cloudinary: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }
