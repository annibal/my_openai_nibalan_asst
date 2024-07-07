import json
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored
from manage_context import set_chat_context, get_chat_context

API_KEY=""
with open(".openai_api_key", 'r') as file:
  API_KEY=file.read()

client = OpenAI(
  api_key=API_KEY,
)

def import_json(path):
    with open(path, 'r') as file:
        data = file.read().replace('\n', '')
        config = json.loads(data)
    return config

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

def f_pretty_print(message):
  try:
    
    if isinstance(message, dict):
      if message["role"] == "tool":
        msg = colored(f'🞚 Tool Result', 'yellow')
        msg += " for "
        msg += colored(message['name'], "yellow")
        msg += ": "
        msg += str(message['content'])
        return msg
    
    if message.role == "tool":
      msg = colored(f'🞚 Tool Result', 'yellow')
      msg += " for "
      msg += colored(message.tool_function_name, "yellow")
      msg += ": "
      msg += str(message.content)
      return msg

    if message.tool_calls:
      msg = ""
      for item in message.tool_calls:
        msg += colored("⌘ Tool Call", "magenta")
        msg += ": "
        msg += colored("name=", "magenta")
        msg += f"'{item.function.name}' "
        msg += colored("args=", "magenta")
        msg += f"'{item.function.arguments}'"
        msg += "\n"
      return msg[:-1]
    
    if message.role == "assistant":
      role = colored("⋖ Assistant", "blue")
      return f"{role}: {message.content}"
    
    if message.role == "user":
      role = colored(f'⮚ You', 'green')
      return f"{role}: {message.content}"
    
    if message.role == "system":
      role = colored(f'⮚ System', 'red')
      return f"{role}: {message.content}"
  except Exception as e:
    print(colored("Error:", "red"))
    print(e)
    print(colored("Message:", "red"))
    print(message)
    return ""

def read_prompt_message():
  try:
    user_input = input(f"{colored(f'⮚ You', 'green')}: ")
    return {"role": "user", "content": user_input}
  except KeyboardInterrupt as e:
    print(colored("\n ⮡  exit \n", "light_grey"))
    return False

def main():
  print(colored("""
  ╔═════════════╗
  ║  ANNIBAL's  ╟─┐
  ║  A.I. chat  ║ │
  ║  assistant  ║ │
  ╚═╤═══════════╝ │
    └─────────────┘
""", "grey"))
  nb = import_json("./assistant_config.json")
  
  messages = []
  messages.append({ "role": "system", "content": nb['instructions'] })

  while True:
    user_message = read_prompt_message()
    if user_message == False:
      break;
    messages.append(user_message)

    chat_response = chat_completion_request(messages, 
      model=nb['model'],
      top_p=nb['top_p'],
      temperature=nb['temperature'],
      tools=nb['tools'],
      tool_choice="required",
      parallel_tool_calls=True,
    )
    
    assistant_message = chat_response.choices[0].message
    messages.append(assistant_message)
    print(f_pretty_print(assistant_message))

    tool_calls = assistant_message.tool_calls
    if tool_calls:
      for item in tool_calls:
        # If true the model will return the name of the tool / function to call and the argument(s)  
        tool_call_id = item.id
        tool_function_name = item.function.name
        tool_query_string = item.function.arguments

        if tool_function_name == "get_instructions":
          ctx = get_chat_context()
          print(f"[ current chat context is '{ctx}' ]")
          results = "respond normally"

          if "Health" in ctx:
            results = "Add warning after message to always seek a doctor in case of doubts."

        if tool_function_name == "set_context":
          set_chat_context(tool_query_string)
          results = '{ success: "true" }'

        if tool_function_name == "get_weather":
          # https://www.7timer.info/doc.php?lang=en
          # https://www.7timer.info/bin/astro.php?lon=113.2&lat=23.1&ac=0&unit=metric&output=json&tzshift=0
          results = '{ temperature: 16, sky: "cloudy" }'

        if tool_function_name == "potter_api":
          # https://potterapi-fedeperin.vercel.app/en/characters?search=Jean
          results = []

        if tool_function_name == "get_trials":
          # https://clinicaltrials.gov/data-api/api
          results = []

        tool_msg = {
          "role": "tool", 
          "tool_call_id": tool_call_id, 
          "name":  tool_function_name, 
          "content": results
        }
        messages.append(tool_msg)
        print(f_pretty_print(tool_msg))

        # print(f"Error: function {tool_function_name} does not exist")

      # get a new response from the model where it can see the function(s) response
      response_with_tool_call = client.chat.completions.create(
          model="gpt-4o",
          messages=messages,
      )
      message_with_tool_call = response_with_tool_call.choices[0].message
      messages.append(message_with_tool_call)
      print(f_pretty_print(message_with_tool_call))

    # end if tool_calls

main()