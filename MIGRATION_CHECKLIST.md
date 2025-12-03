# Airtable to Baserow Migration - Complete Checklist

## Pre-Migration (Day 1)

### Planning
- [ ] Review all migration documents
- [ ] Identify all Airtable dependencies
- [ ] Plan downtime window (if needed)
- [ ] Notify team of migration plan
- [ ] Create backup of Airtable data

### Baserow Setup
- [ ] Create Baserow account (https://baserow.io)
- [ ] Create new database
- [ ] Create 4 tables:
  - [ ] Customer details
  - [ ] Fix it
  - [ ] Recevied email
  - [ ] Received
- [ ] Add fields to each table (see table schema below)
- [ ] Get database ID from URL
- [ ] Get table IDs (hover over table names)
- [ ] Generate API token in Account Settings
- [ ] Test API token with curl

### Documentation
- [ ] Document all table IDs
- [ ] Document all field names
- [ ] Create migration runbook
- [ ] Prepare rollback plan

---

## Table Schema Setup

### Table 1: Customer details

| Field Name | Type | Required | Notes |
|------------|------|----------|-------|
| Name | Text | Yes | Customer name |
| Email | Email | Yes | Customer email |
| Phone | Phone | No | Customer phone |
| VIN | Text | No | Vehicle ID |
| Brand | Text | No | Car brand |
| Plate Number | Text | No | License plate |
| Notes | Long text | No | Additional notes |
| Image | File | No | Damage photos |
| Date and Time | Date | No | Submission time |
| Sent Emails | Text | No | Response tracking |

- [ ] Create all fields
- [ ] Set required fields
- [ ] Test record creation

### Table 2: Fix it

| Field Name | Type | Required | Notes |
|------------|------|----------|-------|
| Name | Text | Yes | Garage name |
| Email | Email | Yes | Garage email |
| Address | Text | No | Garage address |
| Phone | Phone | No | Garage phone |
| Website | URL | No | Garage website |
| Specialties | Text | No | Specialties |
| Reviews | Text | No | Reviews |

- [ ] Create all fields
- [ ] Add test garage records
- [ ] Verify email field is populated

### Table 3: Recevied email

| Field Name | Type | Required | Notes |
|------------|------|----------|-------|
| VIN | Text | No | Vehicle ID |
| Email | Email | No | Sender email |
| Subject | Text | No | Email subject |
| Body | Long text | No | Email body |
| Received At | Date | No | Receipt time |
| Quote | Text | No | Quote amount |

- [ ] Create all fields
- [ ] Test record creation

### Table 4: Received

| Field Name | Type | Required | Notes |
|------------|------|----------|-------|
| Garage Name | Text | No | Garage name |
| Email | Email | No | Garage email |
| Request ID | Text | No | Request ID |
| Quote Amount | Number | No | Quote amount |
| Notes | Long text | No | Notes |
| Status | Single select | No | Status (pending/quoted/declined) |
| Response Date | Date | No | Response date |

- [ ] Create all fields
- [ ] Set up Status options
- [ ] Test record creation

---

## Development (Days 2-5)

### Code Changes

#### Step 1: Update Dependencies
- [ ] Open `backend/requirements.txt`
- [ ] Remove line: `pyairtable`
- [ ] Verify `requests` is present
- [ ] Save file

#### Step 2: Create Baserow Service
- [ ] Create `backend/app/services/baserow_service.py`
- [ ] Copy from `BASEROW_SERVICE_TEMPLATE.py`
- [ ] Implement all methods:
  - [ ] `__init__()`
  - [ ] `_make_request()`
  - [ ] `get_fix_it_garages()`
  - [ ] `create_customer()`
  - [ ] `get_records()`
  - [ ] `update_record()`
  - [ ] `delete_record()`
  - [ ] `store_received_email()`
  - [ ] `record_garage_response()`
  - [ ] `get_record()`
  - [ ] `create_record()`

#### Step 3: Update Environment Variables
- [ ] Open `backend/.env`
- [ ] Remove:
  - [ ] `AIRTABLE_API_KEY`
  - [ ] `AIRTABLE_BASE_ID`
- [ ] Add:
  - [ ] `BASEROW_URL=https://api.baserow.io`
  - [ ] `BASEROW_API_TOKEN=your_token`
  - [ ] `BASEROW_DATABASE_ID=123`
  - [ ] `BASEROW_TABLE_CUSTOMER_DETAILS=456`
  - [ ] `BASEROW_TABLE_FIX_IT=457`
  - [ ] `BASEROW_TABLE_RECEIVED_EMAIL=458`
  - [ ] `BASEROW_TABLE_RECEIVED=459`
- [ ] Save file

#### Step 4: Update Imports
- [ ] File: `backend/app/services/customer_response_service.py`
  - [ ] Line 4: Change import to `baserow_service`
  - [ ] Test import works

- [ ] File: `backend/app/services/email_monitor_service.py`
  - [ ] Line 10: Change import to `baserow_service`
  - [ ] Test import works

- [ ] File: `backend/app/services/fix_it_service.py`
  - [ ] Line 4: Change import to `baserow_service`
  - [ ] Test import works

- [ ] File: `backend/app/api/endpoints/fix_it.py`
  - [ ] Line 111: Change import to `baserow_service`
  - [ ] Test import works

#### Step 5: Verify No Breaking Changes
- [ ] All service methods have same signatures
- [ ] All return values are compatible
- [ ] Error handling is consistent
- [ ] Logging is in place

---

## Testing (Days 6-8)

### Unit Tests

#### Test: get_fix_it_garages()
- [ ] Test returns list
- [ ] Test returns garages with email
- [ ] Test handles pagination
- [ ] Test handles errors
- [ ] Test handles empty results

#### Test: create_customer()
- [ ] Test creates record with required fields
- [ ] Test creates record with optional fields
- [ ] Test returns record_id
- [ ] Test handles invalid email
- [ ] Test handles missing required fields
- [ ] Test handles API errors

#### Test: get_records()
- [ ] Test returns list
- [ ] Test handles pagination
- [ ] Test handles empty results
- [ ] Test handles errors

#### Test: update_record()
- [ ] Test updates single field
- [ ] Test updates multiple fields
- [ ] Test returns updated record
- [ ] Test handles invalid record_id
- [ ] Test handles errors

#### Test: store_received_email()
- [ ] Test creates email record
- [ ] Test handles duplicate detection
- [ ] Test stores all fields
- [ ] Test handles errors

#### Test: record_garage_response()
- [ ] Test creates response record
- [ ] Test stores all fields
- [ ] Test handles errors

### Integration Tests

#### Test: Scheduler Integration
- [ ] Scheduler can fetch garages
- [ ] Scheduler can store emails
- [ ] Scheduler can update records
- [ ] Scheduler handles errors gracefully

#### Test: Email Service Integration
- [ ] Email service can access garages
- [ ] Email service can store responses
- [ ] Email service can update customer records

#### Test: Fix It Service Integration
- [ ] Fix It service can fetch garages
- [ ] Fix It service can create customers
- [ ] Fix It service can send emails

### End-to-End Tests

#### Test: Complete Flow
- [ ] User submits form on frontend
- [ ] Customer record created in Baserow
- [ ] Verify all fields populated correctly
- [ ] Verify images uploaded to Cloudinary
- [ ] Verify emails sent to all garages
- [ ] Simulate garage reply
- [ ] Verify email captured in Baserow
- [ ] Verify scheduler processes email
- [ ] Verify customer receives compiled quotes
- [ ] Verify no data loss

#### Test: Error Scenarios
- [ ] Handle network timeout
- [ ] Handle invalid API token
- [ ] Handle missing table
- [ ] Handle invalid field
- [ ] Handle rate limiting
- [ ] Verify graceful degradation

#### Test: Performance
- [ ] Measure API response times
- [ ] Measure pagination performance
- [ ] Measure email sending time
- [ ] Verify no memory leaks
- [ ] Verify no database locks

---

## Deployment (Days 9-10)

### Pre-Deployment
- [ ] All tests passing
- [ ] Code review completed
- [ ] Documentation updated
- [ ] Rollback plan tested
- [ ] Team notified of deployment

### Staging Deployment
- [ ] Deploy to staging environment
- [ ] Run full test suite
- [ ] Monitor logs for errors
- [ ] Test with real data
- [ ] Verify performance acceptable
- [ ] Get approval from team

### Production Deployment
- [ ] Schedule maintenance window (if needed)
- [ ] Backup current Airtable data
- [ ] Deploy to production
- [ ] Run smoke tests
- [ ] Monitor logs closely
- [ ] Monitor error rates
- [ ] Monitor response times
- [ ] Verify customer submissions working
- [ ] Verify emails being sent
- [ ] Verify data being stored

### Post-Deployment
- [ ] Monitor for 24 hours
- [ ] Check for any errors in logs
- [ ] Verify all systems operational
- [ ] Get team sign-off
- [ ] Document any issues
- [ ] Update runbook

---

## Cleanup (Day 11)

### Code Cleanup
- [ ] Remove old `airtable_service.py` (or keep as backup)
- [ ] Remove any temporary test code
- [ ] Update comments and docstrings
- [ ] Verify no dead code

### Documentation
- [ ] Update README.md
- [ ] Update deployment guide
- [ ] Update API documentation
- [ ] Archive migration documents
- [ ] Update team wiki

### Data Management
- [ ] Export Airtable data as backup
- [ ] Archive old Airtable base
- [ ] Verify Baserow has all data
- [ ] Verify data integrity
- [ ] Delete temporary test records

### Monitoring
- [ ] Set up alerts for API errors
- [ ] Set up alerts for rate limiting
- [ ] Set up alerts for slow queries
- [ ] Monitor for 1 week post-deployment
- [ ] Document any issues found

---

## Rollback Plan (If Needed)

### Immediate Actions
- [ ] Stop all services
- [ ] Revert code changes:
  ```bash
  git checkout backend/app/services/airtable_service.py
  ```
- [ ] Update imports back to `airtable_service`
- [ ] Update `.env` with Airtable credentials
- [ ] Restart backend service

### Verification
- [ ] Test form submission
- [ ] Verify customer record created in Airtable
- [ ] Verify emails sent
- [ ] Verify no errors in logs
- [ ] Notify team of rollback

### Post-Rollback
- [ ] Analyze what went wrong
- [ ] Document issues
- [ ] Plan fixes
- [ ] Schedule retry

---

## Success Criteria

### Functionality
- [ ] All form submissions work
- [ ] All customer records created
- [ ] All emails sent to garages
- [ ] All garage replies captured
- [ ] All customer responses sent
- [ ] No data loss
- [ ] No missing fields

### Performance
- [ ] API response time < 500ms
- [ ] Email sending < 2 seconds per garage
- [ ] Pagination working smoothly
- [ ] No rate limiting issues
- [ ] No timeout errors

### Reliability
- [ ] No errors in logs
- [ ] All tests passing
- [ ] Error handling working
- [ ] Graceful degradation on failures
- [ ] Monitoring alerts working

### Documentation
- [ ] All changes documented
- [ ] Runbook updated
- [ ] Team trained
- [ ] Migration guide archived

---

## Sign-Off

### Development Team
- [ ] Code review completed
- [ ] All tests passing
- [ ] Ready for staging

### QA Team
- [ ] Staging tests completed
- [ ] Performance acceptable
- [ ] Ready for production

### Operations Team
- [ ] Deployment plan reviewed
- [ ] Rollback plan tested
- [ ] Monitoring set up
- [ ] Ready for production

### Management
- [ ] Deployment approved
- [ ] Timeline acceptable
- [ ] Risk acceptable

---

## Contact & Support

### During Migration
- **Lead**: [Your Name]
- **Backup**: [Team Member]
- **Slack Channel**: #garagefy-migration
- **Emergency Contact**: [Phone Number]

### Baserow Support
- **Docs**: https://baserow.io/docs
- **API**: https://api.baserow.io/docs
- **Community**: https://community.baserow.io
- **Issues**: https://github.com/bram2000/baserow/issues

---

## Notes

### What Went Well
- [ ] (To be filled during migration)

### What Could Be Better
- [ ] (To be filled during migration)

### Lessons Learned
- [ ] (To be filled during migration)

### Future Improvements
- [ ] (To be filled during migration)

---

## Appendix: Quick Commands

### Test Baserow Connection
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  https://api.baserow.io/api/database/rows/table/TABLE_ID/
```

### Get Table IDs
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  https://api.baserow.io/api/database/tables/
```

### Get Field IDs
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  https://api.baserow.io/api/database/tables/TABLE_ID/fields/
```

### Run Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Start Backend
```bash
cd backend
python run.py
```

### Check Logs
```bash
tail -f backend/logs/garagefy.log
```

