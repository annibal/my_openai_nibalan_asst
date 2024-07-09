from function_tools.tool_get_instructions import get_instructions
from function_tools.tool_manage_context import set_chat_context, get_chat_context
from function_tools.tool_clinical_trials import list_trials, show_full_trial
from function_tools.tool_get_website import get_website
from function_tools.tool_harry_potter import get_hp_information
from function_tools.tool_weather import get_weather_information
from function_tools.tool_characteristics_memory import set_characteristics
from helpers.terminal_helpers import tprint

# tool call needs thread_id
def handle_tool_call(fn_name, fn_args):
  tprint(f"handling tool call request for '{fn_name}'", verbose=True)
  results = ""

  obj_args = fn_args
  tprint("parsed arguments:", verbose=True)
  tprint(obj_args, verbose=True)

  if fn_name == "get_instructions":
    results = get_instructions(obj_args);

  if fn_name == "set_context":
    results = set_chat_context(obj_args)

  if fn_name == "get_weather":
    results = get_weather_information()

  if fn_name == "potter_api":
    results = get_hp_information()

  if fn_name == "get_website":
    results = get_website(obj_args)

  if fn_name == "get_trials":
    results = list_trials(obj_args)

  if fn_name == "show_trial":
    results = show_full_trial(obj_args)

  if fn_name == "set_characteristics_memory":
    results = set_characteristics(obj_args) # thread_id

  tprint(f"finished tool call with results: '{str(results)}'", verbose=True)
  return str(results)


def handle_flow_instructions(thread_id):
  file_name = f"./temp_chat_data/{thread_id}.json"
  # read
  # if empty: populate with default
  # decide stage
  # create instruction message
  return None