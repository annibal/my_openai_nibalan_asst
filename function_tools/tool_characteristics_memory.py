from helpers.fs_helper import read_obj, write_obj
from helpers.terminal_helpers import tprint

def get_file_name(thread_id):
  return f"./temp_chat_data/{thread_id}.json"

def read_data_characteristics(thread_id):
  file_name = get_file_name(thread_id)
  user_data = read_obj(file_name)

  if user_data == False:
    tprint("No user data found, creating empty", debug=True)
    user_data = {
      "age": None,
      "sex": None,
      "latitude": None,
      "longitude": None,
      "conditions": [],
      "terms": [],
      "has_listed_trials": False,
      "good_trials": [],
      "bad_trials": [],
    }
    write_data_characteristics(user_data, thread_id)

  return user_data

def write_data_characteristics(data, thread_id):
  file_name = get_file_name(thread_id)

  tprint(f"Will write user_data to file '{file_name}':", verbose=True)
  tprint(data, verbose=True)
  write_obj(file_name, data)
  tprint("user_data file successfully saved", verbose=True)



def set_characteristics(data, thread_id="thrd_001_unknown"):
  user_data = read_data_characteristics(thread_id)
  data_keys = data.keys()
  
  # if 'is_remove' in data_keys:
  #   if data['is_remove']:
  #     todo: implement removal of information

  if 'has_listed_trials' in data_keys:
    user_data['has_listed_trials'] = bool(data['has_listed_trials'])

  if 'age' in data_keys:
    user_data['age'] = data['age']

  if 'sex' in data_keys:
    user_data['sex'] = data['sex']

  if 'location' in data_keys:
    user_data['latitude'] = data['location'].split(",")[0]
    user_data['longitude'] = data['location'].split(",")[1]

  if 'condition' in data_keys:
    new_conditions = data['condition'].split(",")
    user_data['conditions'].extend(new_conditions)

  if 'term' in data_keys:
    new_terms = data['term'].split(",")
    user_data['terms'].extend(new_terms)

  if 'bad_trials' in data_keys:
    new_trials = data['bad_trials'].split(",")
    user_data['bad_trials'].extend(new_trials)

  if 'good_trials' in data_keys:
    new_trials = data['good_trials'].split(",")
    user_data['good_trials'].extend(new_trials)

  write_data_characteristics(user_data, thread_id)

  results = '{ success: "true" }'
  return results;