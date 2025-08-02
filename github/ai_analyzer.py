import google.generativeai as genai

from decouple import config
from icecream import ic

API_KEY = config("GEMINI_API_TOKEN")

# Configure the library with your API key
genai.configure(api_key=API_KEY)

# Set up the model
generation_config = {
  "temperature": 0.7,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 256,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    generation_config=generation_config
)

def analyze_commit_with_ai(commit_messages: list[str]) -> str:
    """
    Sends a commit messages to the Gemini API for analysis using the Google GenAI SDK.
    """
    # The prompt remains the same, telling the AI its role and task.
    formatted_commits = "\n".join(f"- {msg.split('/')[-1].strip()}" for msg in commit_messages)
    prompt = f"""
    As an expert programmer and code reviewer, analyze the following Git commit message.
    Provide brief, actionable feedback on its clarity, conciseness, and adherence to
    the conventional commit format (e.g., `<type>: <subject>`).
    If the message can be improved, suggest a better version.

    Commit Message: "{formatted_commits}"

    Your analysis:
    """

    try:
        response = model.generate_content(prompt)
        ic(response.text)
        return response.text.strip()
    except Exception as e:
        # The SDK will raise specific errors, but a general catch-all is fine for now
        print(f"An error occurred while calling the Gemini API: {e}")
        return "Error: Could not get analysis from AI."

