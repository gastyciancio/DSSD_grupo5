from flask import render_template
from app.helpers.bonita_api import get_all_bonita_usernames, get_all_running_cases, get_case_variable_value

def index():    
    collection_creators_dict = get_collection_creators_and_amounts()
    print(collection_creators_dict)
    return render_template('indicators.html', collection_creators_dict=collection_creators_dict)

def get_collection_creators_and_amounts():
    all_running_cases = get_all_running_cases()
    all_running_cases_ids = list(map(lambda case: case['id'], all_running_cases))

    usernames = get_all_bonita_usernames()
    username_created_collections = dict.fromkeys(usernames, 0)
    
    for case_id in all_running_cases_ids:
        creator = get_case_variable_value("/collection_creator", case_id)
        username_created_collections[creator] += 1
    
    return username_created_collections