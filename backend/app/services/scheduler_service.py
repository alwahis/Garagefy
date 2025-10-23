import logging
import asyncio
from typing import Optional
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from .email_monitor_service import email_monitor_service
from .customer_response_service import customer_response_service

logger = logging.getLogger(__name__)

class SchedulerService:
    """Service for scheduling automated tasks"""
    
    def __init__(self):
        self.scheduler: Optional[AsyncIOScheduler] = None
        self.is_running = False
    
    def start(self):
        """Start the scheduler with all automated tasks"""
        if self.is_running:
            logger.warning("Scheduler is already running")
            return
        
        try:
            logger.info("Starting scheduler service")
            
            # Create scheduler
            self.scheduler = AsyncIOScheduler()
            
            # Add job to check emails every 1 minute (starts at :00 seconds)
            self.scheduler.add_job(
                func=self._check_emails_task,
                trigger=IntervalTrigger(minutes=1),
                id='check_emails',
                name='Check inbox for garage responses',
                replace_existing=True,
                max_instances=1
            )
            logger.info("Scheduled email checking task (every 1 minute)")
            
            # Add job to send customer responses every minute (starts at :30 seconds - staggered)
            # Import time for initial delay
            import time
            from datetime import datetime, timedelta
            
            # Calculate delay to start at next :30 second mark
            now = datetime.now()
            delay_seconds = (30 - now.second) % 60
            if delay_seconds < 5:  # If we're very close to :30, wait for next cycle
                delay_seconds += 60
            
            # Schedule with initial delay, then every minute
            self.scheduler.add_job(
                func=self._send_customer_responses_task,
                trigger=IntervalTrigger(minutes=1, start_date=datetime.now() + timedelta(seconds=delay_seconds)),
                id='send_customer_responses',
                name='Send compiled quotes to customers',
                replace_existing=True,
                max_instances=1
            )
            logger.info(f"Scheduled customer response task (every 1 minute, starting in {delay_seconds}s to avoid conflicts)")
            
            # Start the scheduler
            self.scheduler.start()
            self.is_running = True
            logger.info("Scheduler service started successfully")
            
        except Exception as e:
            logger.error(f"Error starting scheduler: {str(e)}", exc_info=True)
            raise
    
    def stop(self):
        """Stop the scheduler"""
        if not self.is_running:
            logger.warning("Scheduler is not running")
            return
        
        try:
            logger.info("Stopping scheduler service")
            if self.scheduler:
                self.scheduler.shutdown(wait=False)
            self.is_running = False
            logger.info("Scheduler service stopped")
        except Exception as e:
            logger.error(f"Error stopping scheduler: {str(e)}", exc_info=True)
    
    async def _check_emails_task(self):
        """Scheduled task to check emails"""
        try:
            logger.info(f"[SCHEDULED] Starting email check at {datetime.now()}")
            result = await email_monitor_service.check_and_process_new_emails(mark_as_read=True)
            
            if result.get('success'):
                logger.info(f"[SCHEDULED] Email check completed: {result.get('emails_processed', 0)} emails processed")
            else:
                logger.error(f"[SCHEDULED] Email check failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            logger.error(f"[SCHEDULED] Error in email check task: {str(e)}", exc_info=True)
    
    async def _send_customer_responses_task(self):
        """Scheduled task to send customer responses"""
        try:
            logger.info(f"[SCHEDULED] Starting customer response check at {datetime.now()}")
            result = await customer_response_service.check_and_send_customer_responses()
            
            if result.get('success'):
                logger.info(f"[SCHEDULED] Customer response check completed: {result.get('responses_sent', 0)} responses sent")
            else:
                logger.error(f"[SCHEDULED] Customer response check failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            logger.error(f"[SCHEDULED] Error in customer response task: {str(e)}", exc_info=True)
    
    def get_status(self) -> dict:
        """Get scheduler status"""
        if not self.is_running:
            return {
                'running': False,
                'jobs': []
            }
        
        jobs = []
        if self.scheduler:
            for job in self.scheduler.get_jobs():
                jobs.append({
                    'id': job.id,
                    'name': job.name,
                    'next_run': str(job.next_run_time) if job.next_run_time else None
                })
        
        return {
            'running': True,
            'jobs': jobs
        }

# Singleton instance
scheduler_service = SchedulerService()
