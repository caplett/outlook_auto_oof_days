from exchangelib import DELEGATE, Account, Credentials, Configuration 
from exchangelib import OofSettings
from datetime import datetime, timedelta
import pytz  # For timezone information
import os
import time
import schedule
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def get_account():
    """Connect to Exchange account using credentials from environment variables"""
    username = os.getenv('OUTLOOK_USERNAME')
    password = os.getenv('OUTLOOK_PASSWORD')
    server = os.getenv('OUTLOOK_SERVER')
    email = os.getenv('OUTLOOK_EMAIL')
    
    if not all([username, password, server, email]):
        logger.error("Missing required environment variables. Please check your .env file.")
        return None
    
    try:
        # Set up credentials and configuration
        credentials = Credentials(username=username, password=password)
        config = Configuration(server=server, credentials=credentials)
        
        # Connect to mailbox
        account = Account(
            primary_smtp_address=email,
            config=config, 
            autodiscover=False, 
            access_type=DELEGATE
        )
        return account
    except Exception as e:
        logger.error(f"Error connecting to Exchange: {e}")
        return None

def get_oof_days():
    """Get the days when OOF should be enabled from environment variables"""
    oof_days_str = os.getenv('OOF_DAYS', '5,6')  # Default to weekend (Sat, Sun)
    try:
        return [int(day) for day in oof_days_str.split(',')]
    except ValueError:
        logger.error("Invalid OOF_DAYS format. Using default (weekends).")
        return [5, 6]  # Default to weekend (Sat, Sun)

def should_enable_oof():
    """Check if OOF should be enabled based on current day of week"""
    oof_days = get_oof_days()
    current_day = datetime.now().weekday()
    return current_day in oof_days

def update_oof_status():
    """Update OOF status based on current day of week"""
    account = get_account()
    if not account:
        return
    
    try:
        # Get current OOF settings
        current_oof = account.oof_settings
        
        # Get timezone for Germany
        tz = pytz.timezone('Europe/Berlin')
        now = datetime.now(tz)
        
        # Check if OOF should be enabled
        enable_oof = should_enable_oof()
        
        if enable_oof and current_oof.state != "Enabled":
            logger.info("Enabling OOF message")
            current_oof.state = "Enabled"
            account.oof_settings = current_oof
            logger.info("OOF message enabled successfully")
        elif not enable_oof and current_oof.state != "Disabled":
            logger.info("Disabling OOF message")
            current_oof.state = "Disabled"
            account.oof_settings = current_oof
            logger.info("OOF message disabled successfully")
        else:
            logger.info(f"No change needed. Current OOF state: {current_oof.state}")
    
    except Exception as e:
        logger.error(f"Error updating OOF status: {e}")

def main():
    """Main function to run the script"""
    logger.info("Starting OOF scheduler")
    
    # Run immediately on startup
    update_oof_status()
    
    # Schedule to run every hour
    schedule.every().hour.do(update_oof_status)
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(600)  # Check every 10 minutes

if __name__ == "__main__":
    main()
