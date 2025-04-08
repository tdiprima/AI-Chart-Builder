# 🥷 Resilient retry logic
import os
from groq import Groq
from tenacity import retry, wait_exponential, stop_after_attempt

# 🔐 Initialize Groq client using environment variable for security
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
def make_groq_request():
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": "Test"}],
        model="meta-llama/llama-4-scout-17b-16e-instruct",
    )
    return response

try:
    result = make_groq_request()
    # OpenAI-style response object
    print("Response from Groq:\n", result.choices[0].message.content)
except Exception as e:
    print(f"Failed after retries: {e}")
