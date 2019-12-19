from flask import Flask, request
from flask_cors import CORS

from nltk import word_tokenize

import pickle as pk
import pandas as pd
import json

# init Flask and enable Cross Origin Resource Sharing
app = Flask(__name__)
CORS(app)

# load the model from the external file
ml_model = pk.load(open('src/model/c_model.pkl', 'rb'))
# load the vectorizer from the external file
vectorizer = pk.load(open("src/model/vectorizer.pkl", "rb"))
# load the mtx catalogue for retriving term name
mtx = pd.read_csv('src/data/MTX_10.3.csv')
#mtx = mtx.apply(lambda x: x.astype(str).str.lower())
mtx.set_index('termCode', inplace=True)

def clean_text(raw_text):
    # 1) Convert to lower case and Tokenize
    tokens = word_tokenize(raw_text.lower())
    # 2) Keep only words (removes punctuation and numbers)
    tokens = [w for w in tokens if w.isalpha()]
    # 3) Stemming
    # tokens = [stemming.stem(w) for w in token_words]
    # Return cleaned text
    return " ".join(tokens)


def interpretCode(code):
    # interpret the foodex2 code
    # split the code between bt and facets
    codes = code.split('#')
    # if there are facets
    if(len(codes) > 1):
        # get the baseterm name
        name =  mtx.loc[codes[0],'termExtendedName']
        # analyse the facets
        if(codes[1]):
            # split the facets by '$'
            facets = codes[1].split('$')
            # for each facet
            for facet in facets:
                # fplit the facet between group of appartenence and code
                comp = facet.split('.')
                # componet the group with the name of the facet
                name += ";" + comp[0] + ":"+mtx.loc[comp[1],'termExtendedName']
    else:
        # get the baseterm name from the list of terms
        name = mtx.loc[codes[-1],'termExtendedName']
    
    return name


def create_json(results):
    # build json for each suggetsed list
    items = []
    for item in results:
        code = item[0]
        name = interpretCode(code)
        empDict = {
            'code': code,
            'name': name,
            'affinity': item[1]
        }
        items.append(empDict)

    return items


@app.route("/getCode", methods=['POST'])
def getCode():
    # get the passed json file
    data = request.get_json()
    # if key doesnt exist return none
    free_text = data['user_text']
    # pre process the inserted free text
    cleaned_desc = [clean_text(free_text)]
    # vectorize the cleaned text with pre-built TfidfVectorizer (removes also stopwords)
    test_data_features = vectorizer.transform(cleaned_desc)
    # predict top best probabilities
    probs = ml_model.predict_proba(test_data_features)
    # zip target class to affinity
    results = zip(ml_model.classes_, probs[0])
    # sort descending and get top 10
    results = sorted(results, key=lambda x: x[1], reverse=True)[:10]
    # create the json
    codes = create_json(results)
    print(json.dumps(codes))
    # return as json
    return json.dumps(codes)


'''
@app.route("/getFacets", methods=['POST'])
def getFacets():
    # get the passed json file
    data = request.get_json()

    # retrieve the selected baseterm index
    btIndex = int(data['btIndex'])

    return ""
'''

if __name__ == "__main__":
    app.run(debug=True)
