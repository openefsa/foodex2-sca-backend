from flask import Flask, request
from flask_cors import CORS

import spacy

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

import pandas as pd
import json

# init Flask and enable Cross Origin Resource Sharing
app = Flask(__name__)
CORS(app)

# it contains all possible models name
global possibleModels
possibleModels = []

# deploy
# max 34
possibleModels = ["F" + "{:02}".format(i) for i in range(1, 34)]
# remove not exsisting models (facet categories)
possibleModels.remove("F05")
possibleModels.remove("F13")
possibleModels.remove("F14")
possibleModels.remove("F15")
possibleModels.remove("F16")
possibleModels.remove("F29")
possibleModels.remove("F30")



# add baseterm
possibleModels.append("baseterm")

# add facets
possibleModels.append("ifFacet")

'''
# add facet categories
possibleModels.append("F02")  # source
possibleModels.append("F04")  # ingredients
possibleModels.append("F10")  # qualitative info
possibleModels.append("F19")  # packaging-material
possibleModels.append("F22")  # preparation production place
possibleModels.append("F27")  # racsource
possibleModels.append("F28")  # process
'''

# load the models from the external file
global models
models = {}
for modelName in possibleModels:
    print("loadModel: "+modelName)
    models[modelName] = spacy.load("src/delaware_models/"+modelName)

# fc_model = spacy.load("../")
# fc01_model = spacy.load("../")
# fcn_model = spacy.load("../")
# fc33_model = spacy.load("../")

# remove punctuation, stop words and not
punctuation = list(string.punctuation)
stopWords = set(stopwords.words('english'))

# load mtx and facet grous for retriving name given code
mtx = pd.read_csv('src/data/MTX_10.3.csv').set_index('code')
categories = pd.read_csv('src/data/facet_categories.csv').set_index('code')


def clean_text(raw_text):
    # 1) Convert to lower case and Tokenize
    tokens = word_tokenize(raw_text.lower())
    # 2) remove stop words
    tokens = [w for w in tokens if w not in stopWords]
    # 3) remove punctuation
    tokens = [w for w in tokens if w not in punctuation]
    # Return cleaned text
    return " ".join(tokens)


def getCategory(text, nlp):
    # return the classes found in the requested model
    doc = models[nlp](text)
    return doc.cats


def getTop(text, nlp, topN):
    # for each class create the tuple <classCode, classProb>
    tuples = getCategory(text, nlp)

    # sort in decreasing order
    tuples = sorted(
        tuples.items(), key=lambda item: item[1], reverse=True)[:topN]

    # chose from which library to get the name
    lib = mtx if nlp != "ifFacet" else categories

    # return topN tuples as list
    predictions = {}
    for k, v in tuples:
        # take only those above threshold
        #if v >= 0.1:
            name = lib.loc[k].values[0]
            predictions[k] = {"name": name, "acc": v}

    return predictions


@app.route("/predict", methods=["GET"])
def predict():
    '''
    @shahaal
    flask API service which return the results given from the model specified in input
    '''
    # get from request the given free text by key
    text = request.args.get("text")
    # get from request the requested model to activate
    model = request.args.get("model")

    # if the requested model is not available
    if model not in possibleModels:
        return

    # pre process the inserted free text
    text = clean_text(text)

    # get top predictions sorted by prob
    res = {model: getTop(text, model, 5)}
    print(res)

    # return as json
    return json.dumps(res)


@app.route("/predictAll", methods=["GET"])
def predictAll():
    '''
    @shahaal
    flask API service which return the results of all models by passing the given free text
    '''
    # get from request the given free text by key
    text = request.args.get("text")

    # pre process the inserted free text
    text = clean_text(text)

    # predict possible baseterms
    basetermResults = {"baseterm": getTop(text, 'baseterm', 5)}
    print(basetermResults)

    # predict possible facet categories
    ifFacetResults = getTop(text, 'ifFacet', 5)
    print(ifFacetResults)

    # for each predicted facet category
    for key in ifFacetResults:
        print(key, '->', ifFacetResults[key])
        # append the list of predicted facets
        ifFacetResults[key]['facets'] = getTop(text, key, 5)

    ifFacetResults = {"facets": ifFacetResults}

    # Merge the dicts as json
    return json.dumps([basetermResults, ifFacetResults])


if __name__ == "__main__":
    app.run(debug=False)
