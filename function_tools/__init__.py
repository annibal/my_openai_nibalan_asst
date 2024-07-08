from function_tools.tool_get_instructions import get_instructions
from function_tools.tool_manage_context import set_chat_context, get_chat_context
from function_tools.tool_clinical_trials import list_trials, show_full_trial
from function_tools.tool_get_website import get_website
from function_tools.tool_harry_potter import get_hp_information
from function_tools.tool_weather import get_weather_information
from function_tools.tool_characteristics_memory import set_characteristics

def handle_tool_call(fn_name, fn_args):
  results = ""

  if fn_name == "get_instructions":
    results = get_instructions();

  if fn_name == "set_context":
    results = set_chat_context(fn_args)

  if fn_name == "get_weather":
    results = get_weather_information(fn_args)

  if fn_name == "potter_api":
    results = get_hp_information(fn_args)

  if fn_name == "get_website":
    results = get_website(fn_args)

  if fn_name == "get_trials":
    results = list_trials(fn_args)

  if fn_name == "show_trial":
    results = show_full_trial(fn_args)

  if fn_name == "set_characteristics_memory":
    results = set_characteristics(fn_args)

  return str(results)