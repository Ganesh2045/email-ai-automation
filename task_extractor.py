from google import genai
from config import GEMINI_API_KEY

# Initialize the new Client
client = genai.Client(api_key=GEMINI_API_KEY)

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

    # Use client.models.generate_content
    response = client.models.generate_content(
        model="gemini-1.5-flash", 
        contents=prompt
    )

    # Access response text and process
    tasks = response.text.strip().split("\n")
    
    return tasks
