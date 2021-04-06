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

from . import api, c
from .utils import get_translation

from nltk.stem import WordNetLemmatizer
from unicodedata import normalize
from nltk import regexp_tokenize
from flask import request
import spacy
import json

asset_path = "api/data/assets/"
# for production
models_path = "models/"

# initialise all possible models name
global possibleModels

possibleModels = ["BT", "CAT"]
# create list facets
possibleModels.extend([
    "F" + "{:02}".format(i) for i in range(1, 34)
    if i not in [5, 13, 14, 15, 16, 29, 30]
])

# TODO only debug
# possibleModels = ["BT", "CAT", "F04", "F28"]

# load the models from the external file
global models
models = {}
for modelName in possibleModels:
    print("loadModel: "+modelName, flush=True)
    models[modelName] = spacy.load(models_path+modelName)


# create queries
query_terms = "SELECT * FROM term WHERE termCode IN (%s)"
query_attrs = "SELECT * FROM attribute WHERE code IN (%s)"


def set_utilities():
    ''' Set up utilites for text cleaning '''

    # read custom punctuation list
    punct = r"[!()\-[\]{};:¼‘“”ªˆ©¤€÷×–¿•…´`'\"\\,<>./?@#$^&*_~=’+]"
    # set word lematizer for removing tense or plural forms
    wnl = WordNetLemmatizer()
    # read custom stop words list
    stop_words = []
    with open(asset_path+'stop_words.csv', 'r') as f:
        for line in f:
            stop_words.append(wnl.lemmatize(line.rstrip('\n')))

    return punct, stop_words, wnl


def clean_text(x):
    ''' clean given text '''
    # unicode and lowercase string
    x = normalize('NFKD', x).encode('ascii', 'ignore').decode('ascii')
    x = x.lower()
    # tokenize using regex (preserve words and values with % or )
    pattern = r'''\d+\.\d+(?:%|°|c)|\d+\.\d+|\d+(?:%|°)|\w+'''
    tokens = regexp_tokenize(x, pattern)
    # remove usless punctuation and words with lenght greater than 1
    tokens = [w for w in tokens if w not in punct and len(w) > 1]
    # remove duplicates (keep order)
    tokens = sorted(set(tokens), key=tokens.index)
    # remove tense or plural forms
    tokens = [wnl.lemmatize(w) for w in tokens]
    # remove stopwords/punct + lemma
    tokens = [w for w in tokens if w not in stop_words]
    # rebuild string
    x = ' '.join(tokens)
    # enable/disable normalization
    # normalizedStr = normalise(x, verbose=False)
    # return none if string empty
    return x if x != '' else None


def get_top(text, nlp, t):
    global models

    # return if not valid threshold
    if not (0.001 <= t <= 99.999):
        return json.dumps({'message': 'Not valid threshold.'})

    # build query based on required model
    query = query_terms if nlp != "CAT" else query_attrs
    # for each class create the tuple <classCode, classProb>
    tuples = models[nlp](text).cats
    # sort in decreasing order
    tuples = sorted(
        tuples.items(), key=lambda item: item[1], reverse=True)
    # keep only codes above threshold max to n items
    predictions = [(k, v) for k, v in tuples if v >= t][:20]
    # initialise results to return
    data_json = []
    # if list of results is not empty
    if predictions:
        # rebuild query based on results
        query = (query % ','.join('?'*len(predictions)))
        # execute query
        c.execute(query, [i[0] for i in predictions])
        # get db column names
        columns = [col[0] for col in c.description]
        # get records from db
        rows = [dict(zip(columns, row)) for row in c.fetchall()]
        # build json
        for k, v in predictions:
            d = [r for r in rows if r['code' if (
                len(k) == 3) else 'termCode'] == k][0]
            d.update({"acc": v})
            data_json.append(d)

    return data_json


@api.route("/predict", methods=["GET"])
def predict():
    '''
    @shahaal
    flask API service which return the results given from the model specified in input
    '''
    # get from request the given free text by key
    desc = request.args.get("desc")
    # get from request the requested model to activate
    model = request.args.get("model").upper()
    # if the requested model is not available
    if model not in possibleModels:
        return json.dumps({'message': 'The model requested is not valid or does not exsists.'})
    # get the treshold from the request
    thld = float(request.args.get("thld"))
    # get from language (if not set use en as dft)
    from_ln = request.args.get("lang")
    # if string is not null translate it
    trsl = get_translation(from_ln, desc) if desc else desc
    # pre process the inserted free text
    cleaned = clean_text(trsl)
    # get top predictions sorted by prob
    res = {model: get_top(cleaned, model, thld)}
    # build final json
    final_json = {"desc":{"orig": desc, "trsl": trsl}}
    final_json.update(res)
    # return as json
    return json.dumps(final_json)


@api.route("/predict_all", methods=["GET"])
def predict_all():
    '''
    @shahaal
    flask API service which return the results of all models by passing the given free text
    '''
    # get from request the given free text by key
    desc = request.args.get("desc")
    # get the treshold from the request
    thld = float(request.args.get("thld"))
    # get from language (if not set use en as dft)
    from_ln = request.args.get("lang")
    # if string is not null translate it
    trsl = get_translation(from_ln, desc) if desc else desc
    # pre process the inserted free text
    cleaned = clean_text(trsl)
    # predict possible baseterms
    bt_res = get_top(cleaned, 'BT', thld)
    # predict possible facet categories
    fc_res = get_top(cleaned, 'CAT', thld)
    # predict possible facets per each category
    for d in fc_res:
        # append the list of predicted facets
        d.update({"facets": get_top(cleaned,  d['code'], thld)})

    # build final json obj
    final_json = {"desc":{"orig": desc, "trsl": trsl}}
    final_json.update({"bt": bt_res, "cat": fc_res})
    # Merge the dicts as json
    return json.dumps(final_json)


# set utilities
punct, stop_words, wnl = set_utilities()
