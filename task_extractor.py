from google import genai
from config import GEMINI_API_KEY

# Force the SDK to use the stable 'v1' endpoint
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
        # CHANGE: Use "gemini-1.5-flash" (no 'models/' prefix)
        # The new SDK handles the routing better this way
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=prompt
        )
        
        # Ensure we handle the response text correctly
        if response.text:
            return response.text.strip().split("\n")
        return []

    except Exception as e:
        print(f"Error: {e}")
        # If it still fails with 404, try "gemini-1.5-flash-latest" 
        # as a fallback inside your code or here:
        return []
