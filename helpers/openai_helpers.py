from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt

API_KEY=""
with open(".openai_api_key", 'r') as file:
  API_KEY=file.read()

client = OpenAI(
  api_key=API_KEY,
)

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, **kwargs):
  try:
    response = client.chat.completions.create(
      messages=messages,
      **kwargs
    )
    return response
  except Exception as e:
    print("Unable to generate ChatCompletion response")
    print(f"Exception: {e}")
    return e

