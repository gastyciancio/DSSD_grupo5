from flask import render_template
from app.helpers.bonita_api import get_all_bonita_designer_usernames, get_all_running_cases, get_case_variable_value, get_all_archived_cases

def index():
    collection_creators_dict = get_collection_creators_and_amounts()
    dates_of_archived_cases = get_dates_of_archived_cases()

    return render_template('indicators.html', collection_creators_dict=collection_creators_dict, dates_of_archived_cases=dates_of_archived_cases)

def get_collection_creators_and_amounts():
    all_running_cases = get_all_running_cases()
    all_running_cases_ids = list(map(lambda case: case['id'], all_running_cases))

    usernames = get_all_bonita_designer_usernames()
    username_created_collections = dict.fromkeys(usernames, 0)
    
    for case_id in all_running_cases_ids:
        creator = get_case_variable_value("/collection_creator", case_id)
        if(creator != ''):
            username_created_collections[creator] += 1
    
    return username_created_collections

def get_dates_of_archived_cases():
    archived_cases = get_all_archived_cases()
    dates_of_archived_cases = []

    if(len(archived_cases) != 0):
        for case in archived_cases:
            dates = {}
            dates['start_date'] = case['start'].split('.', 1)[0][:-3]    #elimino los milisegundos
            dates['end_date'] = case['end_date'].split('.', 1)[0][:-3]
            dates_of_archived_cases.append(dates)
    
    return dates_of_archived_cases