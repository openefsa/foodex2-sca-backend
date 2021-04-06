import os
import uuid
import requests
import sqlite3
import pandas as pd

# TODO only debug, force azure translator key and resource location
'''
os.environ["TRANSLATOR_SUBSCRIPTION_KEY"] = "your_subscription_key"
os.environ["TRANSLATOR_RESOURCE_LOCATION"] = "your_resource_location"
'''

# get translation key and resource location from env variables
subscription_key = os.environ["TRANSLATOR_SUBSCRIPTION_KEY"]
location = os.environ["TRANSLATOR_RESOURCE_LOCATION"]

# set up azure translator url
base_url = 'https://api.cognitive.microsofttranslator.com'
path = '/translate?api-version=3.0'


def get_translation(from_ln, text_input):
    ''' Method used to translate non english text input to english '''

    # if the text input is in english no need to translate
    if from_ln == 'en':
        return text_input
    # set up call parameters
    params = '&from=' + from_ln + '&to=en'
    constructed_url = base_url + path + params
    # set up call header
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    # set the text input in the body request
    body = [{
        'text': text_input
    }]
    # parse the response
    response = requests.post(constructed_url, headers=headers, json=body)
    response = response.json()
    return response[0]['translations'][0]['text']


def check_db(filename):
    ''' check if the mtx database exsist else create it '''
    root_path = 'api/data/mtx/'+filename
    db_path, xlsx_path = root_path+".db", root_path+".xlsx"
    if not os.path.isfile(db_path):
        print('db not exsisting, creating it')
        con = sqlite3.connect(db_path)
        print('db connection correctly instantieted')
        xlsx = pd.ExcelFile(xlsx_path)
        print('loaded xlsx file')
        sheet_names = ['term', 'attribute']
        for name in sheet_names:
            df = xlsx.parse(name)
            df.to_sql(name, con, index=False, if_exists="replace")
            print(f'table {name} created')
        con.commit()
        con.close()
        print('db created successfully')
    else:
        print('db already exsisting')
    return db_path


'''
text_input = "pão de chocolate"
ln_from, ln_to = 'pt', 'en'
response = get_translation(ln_from, text_input)
print(response[0]['translations'][0]['text'])
'''
