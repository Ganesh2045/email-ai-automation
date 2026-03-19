import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("models/gemini-1.5-flash")


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

    response = model.generate_content(prompt)

    tasks = response.text.split("\n")

    return tasks
