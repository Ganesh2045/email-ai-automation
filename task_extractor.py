import re
from google import genai
from google.genai import types 
from config import GEMINI_API_KEY

# Initialize the client
client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(api_version='v1')
)

def clean_task(task_text):
    # Remove leading list markers like "* ", "- ", "1. ", "• "
    cleaned = re.sub(r'^[\*\-\+\s•\d+\.\)]+\s*', '', task_text.strip())
    return cleaned.strip()

def extract_tasks(email_text):
    prompt = f"""
Extract actionable tasks from this email.

PRIORITY RULES

HIGH PRIORITY
- Weekly coding assessments
- CCC LeetCode assessments
- Coding tests
- Deadlines

MEDIUM PRIORITY
- Assignments
- Meetings

LOW PRIORITY
- Reminders

Ignore informational emails.

Return only bullet points.

Example:
[HIGH] Complete CCC LeetCode weekly assessment
[MEDIUM] Attend meeting tomorrow

Email:
{email_text}
"""

    try:
        # These lines must be indented 4 spaces from 'try'
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        
        if response and response.text:
            raw_tasks = response.text.strip().split("\n")
            cleaned_tasks = []
            for task in raw_tasks:
                cleaned = clean_task(task)
                if cleaned:
                    cleaned_tasks.append(cleaned)
            return cleaned_tasks
        return []

    except Exception as e:
        # This 'except' must line up exactly under 'try'
        print(f"Extraction failed: {e}")
        return []

