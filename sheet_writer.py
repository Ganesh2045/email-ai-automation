import gspread
from config import SHEET_NAME

try:
    gc = gspread.service_account(filename="service_account.json")
    sheet = gc.open(SHEET_NAME).sheet1
except FileNotFoundError:
    print("\n" + "="*80)
    print("ERROR: 'service_account.json' is missing in your local project folder!")
    print("To connect to Google Sheets, please create a file named 'service_account.json'")
    print("in this folder and paste your Service Account JSON credentials inside it.")
    print("="*80 + "\n")
    import sys
    sys.exit(1)


def save_tasks(tasks):

    try:
        existing_tasks = set(sheet.col_values(1))
    except Exception as e:
        print(f"Failed to fetch existing tasks to check for duplicates: {e}")
        existing_tasks = set()

    for task in tasks:

        task = task.strip()

        if task != "" and task not in existing_tasks:
            sheet.append_row([task, "Pending"])
            existing_tasks.add(task)