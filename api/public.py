#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# *********************************************************************
# |                                                                    
# | File: \public.py
# | Description: <<desc here>>
# | Project: api
# | Created Date: 25th May 2020
# | Author: Alban Shahaj (shahaal)
# | Email: data.collection@efsa.europa.eu
# | -----------------------------------------------------------------  
# | Last Modified: Thursday, 24th June 2020
# | Modified By: Alban Shahaj (shahaal)
# | -----------------------------------------------------------------  
# | Copyright (c) 2020 European Food Safety Authority (EFSA)
# |                                                                    
# *********************************************************************
###


from . import api
from flask import request

from nltk.tokenize import word_tokenize
import spacy

import pandas as pd
import json
import re


rootPath = "api/asset/"
# "/work-dir/foodex2PreditionDeployed/"
models_path = rootPath + "models/"

# it contains all possible models name
global possibleModels
'''
# add baseterm and ifFacet
possibleModels = ["BT", "CAT"]
# create list facets
possibleModels.extend([
    "F" + "{:02}".format(i) for i in range(1, 34)
    if i not in [5, 13, 14, 15, 16, 29, 30]
])
'''
# TODO only debug
possibleModels = ["BT", "CAT", "F04", "F10", "F28"]

# load the models from the external file
global models
models = {}
for modelName in possibleModels:
    print("loadModel: "+modelName, flush=True)
    models[modelName] = spacy.load(models_path+modelName)


# remove punctuation, stop words and not
punctuation = r"[!()\-[\]{};:'\"\\,<>./?@#$^&*_~=’+°]"
# read custom stop words list
stopWords = []
with open(rootPath+'data/stop_words.csv', 'r') as f:
    stopWords = f.read().split('\n')

# load mtx terms and categories
xlsx = pd.ExcelFile(rootPath+'data/MTX_11.2.xlsx')
terms_data = pd.read_excel(xlsx, 'term')
cats_data = pd.read_excel(xlsx, 'attribute')
mtx_categories = pd.DataFrame(
    cats_data, columns=['code', 'label']).set_index('code')
mtx_terms = pd.DataFrame(terms_data, columns=[
                         'termCode', 'termExtendedName']).set_index('termCode')


"""
def filterDuplicates(tokens):
    ''' filter duplicated words maintaining the order '''

    return sorted(set(tokens), key=tokens.index)
"""


def cleanText(x):
    ''' method used fro cleaning text given in input '''

    # all lower case
    cleanStr = x.lower()
    # remove punctuation
    cleanStr = re.sub(punctuation, " ", cleanStr)
    # tokenization
    tokens = word_tokenize(cleanStr)
    # remove duplicates
    # tokens = filterDuplicates(tokens)
    # remove stop words
    tokens = [w for w in tokens if not w in stopWords]

    # enable/disable normalization
    # normalizedStr = normalise(cleanStr, verbose=False)

    # trim multiple white spaces
    cleanStr = ' '.join(tokens)

    return cleanStr


def getTop(text, nlp, t):
    global models
    # for each class create the tuple <classCode, classProb>
    tuples = models[nlp](text).cats

    # sort in decreasing order
    tuples = sorted(
        tuples.items(), key=lambda item: item[1], reverse=True)

    # chose from which library to get the name
    lib = mtx_terms if nlp != "CAT" else mtx_categories

    # return tuples above threshold as list
    predictions = {}
    for k, v in tuples:
        # take only those above threshold
        if v >= t:
            name = lib.loc[k].values[0]
            predictions[k] = {"name": name, "acc": v}

    return predictions


@api.route("/predict", methods=["GET"])
def predict():
    '''
    @shahaal
    flask API service which return the results given from the model specified in input
    '''
    # get from request the given free text by key
    text = request.args.get("text")
    # get from request the requested model to activate
    model = request.args.get("model")
    # get the treshold from the request
    t = float(request.args.get("threshold"))

    # if the requested model is not available
    if model not in possibleModels:
        return json.dumps("{}")

    # pre process the inserted free text
    text = cleanText(text)

    # get top predictions sorted by prob
    res = {model: getTop(text, model, t)}

    # return as json
    return json.dumps(res)


@api.route("/predictAll", methods=["GET"])
def predictAll():
    '''
    @shahaal
    flask API service which return the results of all models by passing the given free text
    '''
    # get from request the given free text by key
    text = request.args.get("text")
    # get the treshold from the request
    t = float(request.args.get("threshold"))

    # pre process the inserted free text
    text = cleanText(text)

    # predict possible baseterms
    basetermResults = {"baseterm": getTop(text, 'BT', t)}
    
    # predict possible facet categories
    ifFacetResults = getTop(text, 'CAT', t)

    # for each predicted facet category
    for key in ifFacetResults:
        # append the list of predicted facets
        ifFacetResults[key]['facets'] = getTop(text, key, t)

    ifFacetResults = {"facets": ifFacetResults}

    # Merge the dicts as json
    return json.dumps([basetermResults, ifFacetResults])