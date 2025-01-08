import datetime
import logging
import os
import time
#from rich import print
import sqlite3_db
from time_keeper import Timer
from config import Config
from send_notifications import Notification
from email_delivery import Sendgrid_email
from browser import scrape


main_logger = logging.getLogger(__name__)


def main():

    # Initialize Config and Logging Settings
    config = Config()
    config.setup_logging()
    
    # Secrets Variables
    pushover_user_key = config.settings.api.pushover_user_key
    pushover_api_key = config.settings.api.pushover_api_key
    sendgrid_api_key  = config.settings.api.sendgrid_api_key
    birthdate = config.settings.credentials.birthdate
    firstname = config.settings.credentials.firstname
    lastname = config.settings.credentials.lastname

    # Settings Variables
    bot_name = config.settings.bot_name
    stage = config.settings.current_env
    machine_name = config.settings.machine_name
    bot_user_name = config.settings.bot_user_name
    business_unit = config.settings.business_unit
    human_time = config.settings.human_time
    from_email = config.settings.notifications.from_email
    to_email = config.settings.notifications.to_email
    browser = config.settings.applications.browser
    table_name = config.settings.sqlite_db.table_name
    db_file_path = config.settings.sqlite_db.db_file_path
    id = int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    run_date = int(datetime.date.today().strftime("%Y%m%d"))
    time = int(datetime.datetime.now().strftime("%H%M%S"))
    main_logger.info(f" {bot_name} completed config setup")

    # Main Functions
    main_logger.info(f"{bot_name} has begun running")
    timer = Timer()
    start_time = timer.start()
    data = scrape(birthdate=birthdate, firstname=firstname, lastname=lastname, browser= browser)
    email = Sendgrid_email(sendgrid_api_key)
    email.send_email(from_email, to_email, bot_name, data[0])
    elapsed_time = timer.stop()
    success = data[1]
    system_exception = data[2]
    business_exception = data[3]
    total_transactions = data[4]
    error = data[5]
    main_logger.info(f"{bot_name} has captured data")

    # Alerts
    message = f"{bot_name} has run successfully. Excecution time: {elapsed_time}"
    alert = Notification(message,bot_name)
    alert.send_desktop()
    alert.send_push(pushover_user_key, pushover_api_key)
    main_logger.info(f"{bot_name} has sent alert")

    # Database metrics
    dir_name: str = os.path.dirname(__file__)
    db_name: str = bot_name + ".db"
    db_file_path: str = os.path.join(dir_name, db_name)
    db = sqlite3_db.Database(db_file_path)

    columns: list[tuple[str, str]] = [
        ("id", "INTEGER PRIMARY KEY"),
        ("bot_name", "TEXT"),
        ("machine_name", "TEXT"),
        ("environment", "TEXT"),
        ("bot_user_name", "TEXT"),
        ("business_unit", "TEXT"),
        ("run_date", "INTEGER"),
        ("time", "INTEGER"),
        ("elapsed_time", "FLOAT"),
        ("human_time", "FLOAT"),
        ("total_transactions", "INTEGER"),
        ("success", "INTEGER"),
        ("business_exception", "INTEGER"),
        ("system_exception", "INTEGER"),
        ("error", "TEXT")
    ]

    data = [
        id,
        bot_name,
        machine_name,
        stage,
        bot_user_name,
        business_unit,
        run_date,
        time,
        elapsed_time,
        human_time,
        total_transactions,
        success,
        business_exception,
        system_exception,
        error
    ]

    db.create_table(table_name, columns)
    db.execute_insert(table_name, data)
    main_logger.info(f"{bot_name} has tracked metrics")
    main_logger.info(f"{bot_name} has completed")

if __name__ == "__main__":
    main()
