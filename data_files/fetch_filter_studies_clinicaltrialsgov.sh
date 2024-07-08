(
  URL="https://clinicaltrials.gov/api/v2/studies"

  # Limit the amount of returned studies (capped to 1000)
  QS_PAGE_SIZE=1000

  # Filter the studies by specific statuses
  QS_STATUSES=(
    # ┏🠊 Participants are not yet being recruited.
    "NOT_YET_RECRUITING"
    # ┏🠊 Participants are currently being recruited,
    # ┃   whether or not any participants have yet
    # ┃   been enrolled.
    "RECRUITING"
    # ┏🠊 Participants are being (or will be)
    # ┃   selected from a predetermined
    # ┃   population.
    # "ENROLLING_BY_INVITATION"
    # ┏🠊 Study is continuing, meaning participants
    # ┃   are receiving an intervention or being
    # ┃   examined, but new participants are not
    # ┃   currently being recruited or enrolled.
    # "ACTIVE_NOT_RECRUITING"
    # ┏🠊 The study has concluded normally;
    # ┃   participants are no longer receiving
    # ┃   an intervention or being examined.
    # "COMPLETED"
    # ┏🠊 Study halted prematurely but might
    # ┃   potentially resume.
    # "SUSPENDED"
    # ┏🠊 Study halted prematurely and will not resume;
    # ┃   participants are no longer being examined or
    # ┃   receiving intervention.
    # "TERMINATED"
    # ┏🠊 Study halted prematurely, prior to enrollment
    # ┃   of first participant.
    # "WITHDRAWN"
    # ┏🠊 Expanded Access is currently available.
    # "AVAILABLE"
    # ┏🠊 Expanded Access was previously available,
    # ┃   is NOT currently available,
    # ┃   is NOT expected to be available in the future.
    # "NO_LONGER_AVAILABLE"
    # ┏🠊 Expanded Access was previously available,
    # ┃   is NOT currently available,
    # ┃   is expected to be available in the future.
    # "TEMPORARILY_NOT_AVAILABLE"
    # ┏🠊 Expanded Access was previously available,
    # ┃   is NOT currently available,
    # ┃   because the product has been approved,
    # ┃   licensed, or cleared by the FDA.
    # "APPROVED_FOR_MARKETING"
    # ┏🠊 Study has results, but they are being kept
    #     secret from the public for some reason.
    # "WITHHELD"
    # ┏🠊 A study whose last known status was either:
    #     - recruiting;
    #     - not yet recruiting;
    #     - active, not recruiting
    #     but passed its completion date, and
    #     the status has not been last verified
    #     within the past 2 years.
    # "UNKNOWN"
  )

  # Geo: only show studies that have an location
  #   close to a certaing place.
  #   provide a POINT with latitude and longitude:
  QS_GEO="47.611351,-122.337297"
  #   and the maximum distance from that POINT,
  #   in miles (12mi) or kilometers (12km):
  QS_DIST="13mi"

  # Some preset filters i left, for studies that
  # accept in a range of age, and an sex.
  QS_FILTER=(
    # "AREA[MinimumAge]RANGE[MIN, 18 years]"
    "AREA[MinimumAge]RANGE[MIN, 29 years]"
    "AREA[MaximumAge]RANGE[29 years, MAX]"
    # "AREA[MaximumAge]RANGE[40 years, MAX]"
    "AREA[Sex]Male"
    # "AREA[Sex]Female"
  )

  # Only return these fields:
  QS_FIELDS=(
    "NCTId|BriefTitle|OfficialTitle"
    "BriefSummary|DetailedDescription"
    "OverallStatus|StartDate"
    "PrimaryCompletionDate|CompletionDate|StudyFirstSubmitDate|LastUpdateSubmitDate"
    "ConditionsModule"
    "EligibilityCriteria|HealthyVolunteers|Sex|MinimumAge|MaximumAge"
    "EnrollmentInfo"
  )

  # Conditions will search for these strings
  # in study's fields:
  # - Condition
  # - BriefTitle
  # - OfficialTitle
  # - Term and AncestorTerm system mesh (?)
  # - Keyword
  # - NCTId.
  QS_CONDITIONS=(
    "marstacimab"
    # "lung cancer"
    # "(head OR neck)"
    # "pain"
  )

  # Calls the API for the studies.
  # - this $(IFS="|"; echo "${arr[*]}") turns this ("one" "two") into "one|two".
  # - --data-urlencode turns "a=one|two" into "a=one%7Ctwo".
  curl -G $URL \
  -X GET \
  -H "accept: application/json" \
  --data-urlencode "format=json" \
  --data-urlencode "countTotal=true" \
  --data-urlencode "pageSize=$QS_PAGE_SIZE" \
  --data-urlencode "query.cond=$(IFS=" AND "; echo "${QS_CONDITIONS[*]}")" \
  --data-urlencode "filter.overallStatus=$(IFS="|"; echo "${QS_STATUSES[*]}")" \
  --data-urlencode "filter.geo=distance($QS_GEO,$QS_DIST)" \
  --data-urlencode "filter.advanced=$(IFS=" AND "; echo "${QS_FILTER[*]}")" \
  --data-urlencode "fields=$(IFS="|"; echo "${QS_FIELDS[*]}")" \
  --verbose
)