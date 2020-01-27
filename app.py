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
bt_model = pk.load(open("src/model/bt_model.pkl", "rb"))
fc_model = pk.load(open("src/model/fc_model.pkl", "rb"))
# load the vectorizer from the external file
bt_vectorizer = pk.load(open("src/model/bt_vectorizer.pkl", "rb"))
fc_vectorizer = pk.load(open("src/model/fc_vectorizer.pkl", "rb"))
# create an object of stemming function
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("english")


def clean_text(raw_text):
    # 1) Convert to lower case and Tokenize
    tokens = word_tokenize(raw_text.lower())
    # 2) Keep only words (removes punctuation and numbers)
    tokens = [w for w in tokens if w.isalpha()]
    # 3) Stemming
    tokens = [stemmer.stem(w) for w in tokens]
    # Return cleaned text
    return " ".join(tokens)


def split_bt(item):
    # the method split the information for building the json
    # item 0: "name:code"; item 1: "affinity"
    info = item[0].split(":")
    return info[0], info[1], item[1]


def split_fc(item):
    # the method split the information for building the json
    # item 0: "name:code"; item 1: "affinity"
    info = item[0].split(":")
    return info[0], info[1], item[1]


def create_bt_json(results):
    # build json for each suggetsed list
    items = []
    for item in results:
        name, code, affinity = split_bt(item)
        empDict = {"code": code, "name": name, "affinity": affinity}
        items.append(empDict)

    return items


def create_fc_json(results):
    # build json for each suggetsed list
    '''
    items = []
    for item in results:
        F01, F02, F03, F04, F06, F07, F08, F09, F10, F11, F12, F17, F18, F19, F20, F21, F22, F23, F24, F25, F26, F27, F28, F29, F30, F31, F32, F33, affinity = split_fc(
            item
        )
        empDict = {"code": code, "name": name, "affinity": affinity}
        items.append(empDict)

    return items
    '''


@app.route("/predictBaseterm", methods=["POST"])
def predictBaseterm():
    # get the passed json file
    data = request.get_json()
    # if key doesnt exist return none
    free_text = data["user_text"]
    # pre process the inserted free text
    cleaned_desc = [clean_text(free_text)]
    # vectorize the cleaned text with pre-built TfidfVectorizer (removes also stopwords)
    test_data_features = bt_vectorizer.transform(cleaned_desc)
    # predict top best probabilities
    probs = bt_model.predict_proba(test_data_features)
    # zip target class to affinity
    results = zip(bt_model.classes_, probs[0])
    # print(results)
    # sort descending and get top 10
    results = sorted(results, key=lambda x: x[1], reverse=True)[:10]
    # create the json
    codes = create_bt_json(results)
    # print(json.dumps(codes))
    # return as json
    return json.dumps(codes)


@app.route("/predictFacets", methods=["POST"])
def predictFacets():
    # get the passed json file
    data = request.get_json()
    # if key doesnt exist return none
    text = data["bt_user_text"]
    # vectorize the cleaned text with pre-built TfidfVectorizer (removes also stopwords)
    test_data_features = fc_vectorizer.transform(text)
    # predict top best probabilities
    probs = fc_model.predict_proba(test_data_features)
    # zip target class to affinity
    results = zip(fc_model.classes_, probs[0])
    # sort descending and get top 10
    results = sorted(results, key=lambda x: x[1], reverse=True)[:10]
    # transform to dataframe for better handling the data
    fc = pd.DataFrame(results)
    # create the json
    codes = create_fc_json(fc)
    # print(json.dumps(codes))
    # return as json
    return json.dumps(codes)


"""
@app.route("/getFacets", methods=['POST'])
def getFacets():
    # get the passed json file
    data = request.get_json()

    # retrieve the selected baseterm index
    btIndex = int(data['btIndex'])

    return ""
"""

if __name__ == "__main__":
    app.run(debug=True)
