import schedule
import time

from gmail_auth import gmail_auth
from email_reader import get_emails
from task_extractor import extract_tasks
from sheet_writer import save_tasks
from config import CHECK_INTERVAL_MINUTES

service = gmail_auth()


def job():

    print("Checking emails...")

    emails = get_emails(service)

    for email in emails:

        tasks = extract_tasks(email)

        save_tasks(tasks)

    print("Tasks updated.")


schedule.every(CHECK_INTERVAL_MINUTES).minutes.do(job)

print("Automation started...")

while True:

    schedule.run_pending()

    time.sleep(1)