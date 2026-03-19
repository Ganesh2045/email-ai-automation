from google import genai
from google.genai import types  # <--- Add this line
from config import GEMINI_API_KEY

# Initialize the client with the forced 'v1' API version
client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(api_version='v1')
)
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
            # CHANGE: Use the explicit version '001' or '002'
            response = client.models.generate_content(
                model="gemini-1.5-flash-001", 
                contents=prompt
            )
            
            if response and response.text:
                return response.text.strip().split("\n")
            return []
    
        except Exception as e:
            print(f"Extraction failed: {e}")
            return []
