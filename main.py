from gmail_auth import gmail_auth
from email_reader import get_unread_emails, mark_as_read
from task_extractor import extract_tasks
from sheet_writer import save_tasks

service = gmail_auth()


def job():

    print("Checking emails...")

    emails = get_unread_emails(service)

    if not emails:
        print("No new unread emails found.")
        return

    for email in emails:
        print(f"Processing email: {email['id']}...")
        tasks = extract_tasks(email["snippet"])

        if tasks:
            print(f"Extracted tasks: {tasks}")
            save_tasks(tasks)
        else:
            print("No tasks extracted from this email.")

        mark_as_read(service, email["id"])
        print(f"Email {email['id']} processed and marked as read.")

    print("Tasks updated.")


if __name__ == "__main__":
    print("Automation started...")
    job()

