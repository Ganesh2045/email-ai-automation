import gspread
from config import SHEET_NAME

gc = gspread.service_account(filename="service_account.json")

sheet = gc.open(SHEET_NAME).sheet1


def save_tasks(tasks):

    for task in tasks:

        task = task.strip()

        if task != "":
            sheet.append_row([task, "Pending"])