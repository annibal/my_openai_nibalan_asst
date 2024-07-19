from helpers.fs_helper import read_obj
from function_tools.tool_characteristics_memory import set_characteristics, read_data_characteristics

def get_missing_parameters_message(data):
  has_age = bool(data['age'])
  has_sex = bool(data['sex'])
  has_latitude = bool(data['latitude'])
  has_longitude = bool(data['longitude'])
  has_conditions = bool(data['conditions'])
  has_terms = bool(data['terms'])

  missing_info = []
  is_missing_info = False
  if not has_age:
    missing_info.append("age")
    is_missing_info = True

  if not has_sex:
    missing_info.append("sex")
    is_missing_info = True

  if not has_latitude:
    missing_info.append("latitude")
    is_missing_info = True

  if not has_longitude: 
    missing_info.append("longitude")
    is_missing_info = True

  if not has_conditions:
    missing_info.append("conditions")

  if not has_terms:
    missing_info.append("terms")

  if is_missing_info:
    return "To list trials, you need to know at least the " + missing_info.join(", ") + " from the user"
  
  return False


def list_trials(filters, thread_id):
  data = read_data_characteristics(thread_id)

  missing_info_msg = get_missing_parameters_message(data)
  if not missing_info_msg == False:
    return missing_info_msg
  

  # age
  # sex
  # location
  # distance
  # distance_unit
  # study_type
  # condition
  # term
  # ...
  
  # https://clinicaltrials.gov/data-api/api
  # ?format=json&countTotal=true&pageSize=1000&query.cond=marstacimab&filter.overallStatus=NOT_YET_RECRUITING|RECRUITING&filter.geo=distance(47.611351,-122.337297,13mi)&filter.advanced=AREA[MinimumAge]RANGE[MIN,+29+years]+AREA[MaximumAge]RANGE[29+years,+MAX]+AREA[Sex]Male&fields=NCTId|BriefTitle|OfficialTitle|BriefSummary|DetailedDescription|OverallStatus|StartDate|PrimaryCompletionDate|CompletionDate|StudyFirstSubmitDate|LastUpdateSubmitDate|ConditionsModule|EligibilityCriteria|HealthyVolunteers|Sex|MinimumAge|MaximumAge|EnrollmentInfo

  # https://clinicaltrials.gov/api/v2/studies

  # NOT AREA[LastKnownStatus]MISSING
  # AREA[MinimumAge]MISSING OR AREA[MaximumAge]MISSING OR AREA[Sex]MISSING

  #   {
  #     "format": "json",
  #     "pageToken": "NF0g5JaPlvE",
  #     "countTotal": "true",
  #     "pageSize": "1000",
  #     "query.cond": "marstacimab",
  #     "filter.overallStatus": "NOT_YET_RECRUITING|RECRUITING",
    #     aka: filter.advanced = (AREA[OverallStatus]not_yet_recruiting OR AREA[OverallStatus]recruiting)
  #     "filter.geo": "distance(47.611351,-122.337297,13mi)",
  #     "filter.advanced": "AREA[MinimumAge]RANGE[MIN, 29 years] AND AREA[MaximumAge]RANGE[29 years, MAX] AND (AREA[Sex]all OR AREA[Sex]male OR AREA[Sex]female) AND (AREA[StudyType]interventional OR AREA[StudyType]observational)",
  #     "fields": "NCTId|BriefTitle|OfficialTitle|BriefSummary|DetailedDescription|OverallStatus|StartDate|PrimaryCompletionDate|CompletionDate|StudyFirstSubmitDate|LastUpdateSubmitDate|ConditionsModule|EligibilityCriteria|HealthyVolunteers|Sex|MinimumAge|MaximumAge|EnrollmentInfo"
  # }

  results = []

  # if len(results) > 100:
  if 'conditions' in data.keys() and len(data['conditions']) > 3:
    mocked_7_trials_result = read_obj("./data_files/example_dump_7_trials.json")
    set_characteristics({ "has_listed_trials": True }, thread_id)
    return mocked_7_trials_result
  
  return "Too many trials were found, ask another question about either the user's conditions, clinical terms etc., to further narrow down the trials"

def show_full_trial(id):
  
  mocked_7_trials_result = read_obj("./data_files/example_dump_7_trials.json")
  trial = filter(lambda x: x['protocolSection']['identificationModule']['nctId'] == id, mocked_7_trials_result['studies'])
  return trial

  # https://clinicaltrials.gov/data-api/api
  # results = []
  # return results;