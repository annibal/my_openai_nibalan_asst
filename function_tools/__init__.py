import asyncio
import json
from function_tools.tool_get_instructions import get_instructions
from function_tools.tool_manage_context import set_chat_context, get_chat_context
from function_tools.tool_clinical_trials import list_trials, show_full_trial
from function_tools.tool_get_website import get_website
from function_tools.tool_harry_potter import get_hp_information
from function_tools.tool_weather import get_weather_information
from function_tools.tool_characteristics_memory import set_characteristics, read_data_characteristics
from helpers.terminal_helpers import tprint

# tool call needs thread_id
async def handle_tool_call(fn_name, fn_args, thread_id="thrd_000_unknown"):
  tprint(f"handling tool call request for '{fn_name}'", verbose=True)
  results = ""

  obj_args = json.loads(fn_args)
  tprint("parsed arguments:", verbose=True)
  tprint(obj_args, verbose=True)

  # Deactivated
  if fn_name == "get_instructions":
    results = get_instructions(obj_args);

  # Deactivated
  if fn_name == "set_context":
    results = set_chat_context(obj_args['context'])

  # Active
  if fn_name == "get_weather":
    results = get_weather_information(
      lat=obj_args['location'].split(",")[0],
      lon=obj_args['location'].split(",")[0],
      unit=obj_args['unit'],
      date=obj_args['date']
    )

  # Deactivated
  if fn_name == "potter_api":
    results = get_hp_information(
      search=obj_args['search'],
      language=obj_args['language'],
      entity=obj_args['entity'],
    )

  # Not Implemented
  if fn_name == "get_website":
    results = get_website(obj_args)

  # Deactivated
  if fn_name == "get_trials":
    results = list_trials(obj_args, thread_id)

  # Active
  if fn_name == "show_trial":
    results = show_full_trial(obj_args['nctid'])

  # Active
  if fn_name == "save_characteristics":
    results = set_characteristics(obj_args, thread_id)

  tprint(f"finished tool call with results: '{str(results)}'", verbose=True)
  return str(results)


async def handle_flow_instructions(thread_id):
  data = read_data_characteristics(thread_id)

  has_age = bool(data['age'])
  has_sex = bool(data['sex'])
  has_latitude = bool(data['latitude'])
  has_longitude = bool(data['longitude'])
  has_conditions = bool(data['conditions'])
  has_terms = bool(data['terms'])
  has_bad_trials = bool(data['bad_trials'])
  has_good_trials = bool(data['good_trials'])

  if has_age and has_sex and has_latitude and has_longitude and not has_conditions and not has_terms:
    return "On the user's next message, you can already search for trials"
  
  if has_age and has_sex and has_latitude and has_longitude and has_conditions and has_terms:
    return "You must search for trials, but only after the next message."
  

  # if curr_count_trials > 20:
  #   return "Inform the user that there's still too many trials, ask for more information"

  return None