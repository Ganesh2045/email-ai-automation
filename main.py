from gmail_auth import gmail_auth
from email_reader import get_unprocessed_emails, mark_as_processed, get_or_create_label
from task_extractor import extract_tasks
from sheet_writer import save_tasks

service = gmail_auth()


def job():

    print("Checking emails...")

    label_id = get_or_create_label(service)
    if not label_id:
        print("Could not retrieve or create the 'Task-Extracted' label. Aborting job.")
        return

    emails = get_unprocessed_emails(service)

    if not emails:
        print("No new unprocessed emails found in INBOX.")
        return

    for email in emails:
        print(f"Processing email: {email['id']}...")
        tasks = extract_tasks(email["snippet"])

        if tasks:
            print(f"Extracted tasks: {tasks}")
            save_tasks(tasks)
        else:
            print("No tasks extracted from this email.")

        mark_as_processed(service, email["id"], label_id)
        print(f"Email {email['id']} processed and marked with 'Task-Extracted' label.")

    print("Tasks updated.")


if __name__ == "__main__":
    print("Automation started...")
    job()


