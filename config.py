import os

# This looks for a secret named "GEMINI_API_KEY" in GitHub Actions
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

SHEET_NAME = "EmailTasks"
CHECK_INTERVAL_MINUTES = 10
