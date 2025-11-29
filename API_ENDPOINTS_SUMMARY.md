# Garagefy API Endpoints Summary

## ✅ Backend Status: RUNNING
- **URL:** http://localhost:8099
- **Health:** ✅ Healthy
- **API Docs:** http://localhost:8099/docs

---

## 📊 Available GET Endpoints (Already Pushed)

### Health & Status
- **GET /health** ✅ WORKING
  - Returns: `{"status": "healthy"}`
  - Purpose: Check if API is running

- **GET /api/fix-it/status** ✅ WORKING
  - Returns: Service status and scheduler info
  - Purpose: Check Fix it service status
  - Response includes:
    - Scheduler running status
    - Scheduled jobs and next run times

- **GET /api/fix-it/test-garages** ✅ WORKING
  - Returns: List of garages from Baserow "Fix it" table
  - Purpose: Test Baserow connectivity
  - Current Status: **0 garages found** (table is empty)

### Quotes Endpoints
- **GET /api/quotes** - Get all quotes
- **GET /api/quotes/{id}** - Get specific quote

### Garage Responses
- **GET /api/garage-responses** - Get all garage responses

---

## 📝 Available POST Endpoints

### Service Requests
- **POST /api/service-requests** - Submit service request with images

### Fix It Operations
- **POST /api/fix-it/check-emails** - Check inbox for garage responses
- **POST /api/fix-it/send-customer-responses** - Send compiled quotes to customers

### Quotes
- **POST /api/quotes** - Create new quote

### Garage Responses
- **POST /api/garage-responses** - Create garage response

---

## 🔄 Scheduler Status

The backend has 2 scheduled tasks running:

1. **Check inbox for garage responses**
   - Runs every 1 minute
   - Next run: 2025-11-28 15:05:22

2. **Send compiled quotes to customers**
   - Runs every 1 minute
   - Next run: 2025-11-28 15:04:30

---

## ⚠️ Current Status

### What's Working ✅
- Backend API is running
- All endpoints are accessible
- Baserow connection is established
- Email service is authenticated
- Scheduler is running
- Background tasks are configured

### What Needs Data ⚠️
- **Garages table is empty** - No garages in Baserow "Fix it" table
- Need to add garage data to proceed with quote requests

---

## 🚀 Next Steps

### 1. Add Garages to Baserow
You need to populate the "Fix it" table in Baserow with garage data:
- Garage name
- Email address
- Phone number
- Address
- Website (optional)
- Specialties (optional)

### 2. Test the API
Visit: http://localhost:8099/docs

### 3. Submit a Service Request
Use the `/api/service-requests` endpoint to submit a quote request

### 4. Monitor Emails
The scheduler will automatically:
- Check for garage responses every minute
- Send compiled quotes to customers

---

## 📋 API Testing Commands

### Test Health
```powershell
Invoke-WebRequest -Uri http://localhost:8099/health -Method Get
```

### Test Fix It Status
```powershell
Invoke-WebRequest -Uri http://localhost:8099/api/fix-it/status -Method Get
```

### Test Garages
```powershell
Invoke-WebRequest -Uri http://localhost:8099/api/fix-it/test-garages -Method Get
```

---

## 📚 Full API Documentation

Visit: **http://localhost:8099/docs**

This provides interactive Swagger UI where you can:
- See all endpoints
- View request/response schemas
- Test endpoints directly
- View error responses

---

**Status:** ✅ Backend Ready  
**Last Updated:** 2025-11-28 15:03  
**All Endpoints:** Accessible and responding
