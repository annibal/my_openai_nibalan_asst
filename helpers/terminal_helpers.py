
from termcolor import colored

def print_header():
  print(colored("""
  ╔═════════════╗
  ║  ANNIBAL's  ╟─┐
  ║  A.I. chat  ║ │
  ║  assistant  ║ │
  ╚═╤═══════════╝ │
    └─────────────┘
""", "grey"))
  
def read_prompt_message():
  try:
    user_input = input(f"{colored(f'⮚ You', 'green')}: ")
    return {"role": "user", "content": user_input}
  except KeyboardInterrupt as e:
    print(colored("\n ⮡  exit \n", "light_grey"))
    return False
  
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