import sys
import os
import time
import datetime
from termcolor import colored

is_debug = False
is_verbose = False



def print_header():
  print(colored("""
  ╔═════════════╗
  ║  ANNIBAL's  ╟─┐
  ║  A.I. chat  ║ │
  ║  assistant  ║ │
  ╚═╤═══════════╝ │
    └─────────────┘
""", "grey"))
  
presets = {
  'user':         { 'color': 'green',    'title': 'You',          'icon': '⮚' },
  'assistant':    { 'color': 'blue',     'title': 'Assistant',    'icon': '⋖' },
  'system':       { 'color': 'red',      'title': 'System',       'icon': '⌘' },
  'tool_call':    { 'color': 'magenta',  'title': 'Tool Call',    'icon': '┗🠊 ◯' },
  'tool_result':  { 'color': 'yellow',   'title': 'Tool Result',  'icon': '┗🠊 ⦿' },
  'debug':        { 'color': 'cyan',     'title': 'Debug',        'icon': '⎇' },
  'default':      { 'color': 'white',    'title': 'Log',          'icon': '∴' },
}

def get_role_header(role):
  defs = presets['default']
  if role in presets.keys():
    defs = presets[role]
  
  icon = defs['icon']
  title = colored(f"{icon} {defs['title']}", defs['color'])
  return title


def read_prompt_message():
  try:
    tprint("wait for user prompt message", verbose=True)
    role = get_role_header("user")
    user_input = input(f"{role}: ").strip()
    
    if user_input.lower().startswith("system: "):
      tprint("treating prompt message with system role instead of user", verbose=True)
      return {"role": "system", "content": user_input.removeprefix("system: ")}
    
    tprint("prompt message received", verbose=True)
    return {"role": "user", "content": user_input}
  
  except KeyboardInterrupt as e:
    print(colored("\n┗🠊 exit() \n", "light_grey"))
    return False
  
def tprint(str, debug=False, verbose=False, header=True):
  global is_debug
  global is_verbose

  if debug:
    if not is_debug:
      return
    if not header:
      print(str)
      return
    str_header = get_role_header("debug")
    print(f"{str_header}: {str}")
    return
  
  if verbose:
    if not is_verbose:
      return
    if not header:
      print(str)
      return
    str_header = get_role_header("default")
    str_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{str_header} [{str_datetime}] {str}")
    return

  print(str)

def fmt_msg(message):
  try:
    
    if isinstance(message, dict):
      if message["role"] == "tool":
        msg = get_role_header("tool_result")
        msg += " for "
        msg += colored(message['name'], "yellow")
        msg += ": "
        msg += str(message['content'])
        return msg
      
      if message["role"] == "assistant":
        role = get_role_header("assistant")
        return f"{role}: {message['content']}"
      
      if message["role"] == "user":
        role = get_role_header("user")
        return f"{role}: {message['content']}"
      
      if message["role"] == "system":
        role = get_role_header("system")
        return f"{role}: {message['content']}"
    
    if message.role == "tool":
      msg = get_role_header("tool_result")
      msg += " for "
      msg += colored(message.tool_function_name, "yellow")
      msg += ": "
      msg += str(message.content)
      return msg

    if message.tool_calls:
      msg = ""  
      for item in message.tool_calls:
        msg += get_role_header("tool_call")
        msg += ": "
        msg += colored("name=", "magenta")
        msg += f"'{item.function.name}' "
        msg += colored("args=", "magenta")
        msg += f"'{item.function.arguments}'"
        msg += "\n"
      return msg[:-1]
    
    if message.role == "assistant":
      role = get_role_header("assistant")
      return f"{role}: {message.content}"
    
    if message.role == "user":
      role = get_role_header("user")
      return f"{role}: {message.content}"
    
    if message.role == "system":
      role = get_role_header("system")
      return f"{role}: {message.content}"
    
  except Exception as e:
    print(colored("⛒ Error: ", "red"))
    print(e)
    print(colored("⋙ Message: ", "red"))
    print(message)
    return ""

def parse_args():
  global is_debug
  global is_verbose

  n = len(sys.argv)
  for i in range(1, n):
    if (sys.argv[i] == "--debug"):
      is_debug = True
      tprint("Debug Enabled", debug=True)
    if (sys.argv[i] == "--verbose"):
      is_verbose = True
      tprint("Verbose Enabled", verbose=True)