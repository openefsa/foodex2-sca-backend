# file used to test model

import spacy
from nltk import word_tokenize

import pandas as pd
import re

rootPath = "services/main/"
# "/work-dir/foodex2PreditionDeployed/"
models_path = rootPath + "models/"

global possibleModels
possibleModels = ["BT"]

# load the model from the external file
global models
models = {}
for modelName in possibleModels:
    print("loadModel: "+modelName, flush=True)
    models[modelName] = spacy.load(models_path+modelName)


# remove punctuation, stop words and not
punctuation = r"[!()\-[\]{};:'\"\\,<>./?@#$^&*_~=’+°]"
# read custom stop words list
stopWords = []
with open(rootPath+'asset/stop_words.csv', 'r') as f:
    stopWords = f.read().split('\n')


# load mtx terms and categories
xlsx = pd.ExcelFile(rootPath+'data/MTX_11.1.xlsx')
terms_data = pd.read_excel(xlsx, 'term')
cats_data = pd.read_excel(xlsx, 'attribute')
mtx_categories = pd.DataFrame(
    cats_data, columns=['code', 'label']).set_index('code')
mtx_terms = pd.DataFrame(terms_data, columns=[
                         'termCode', 'termExtendedName']).set_index('termCode')


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

# free text food description (english)
'''
description = ["oat",
               "strawberry flavour milk",
               "chocolate with cow milk semi skimed and sterlised",
               "apple pie",
               "pie with apples",
               "white chocolate with hazelnuts"]
'''
description = "white chocolate with nuts"
#description = "pizza with spinach"

# pre process the inserted free text
cleaned_desc = cleanText(description)

####################################################################

# predict possible baseterms
basetermResults = {"baseterm": getTop(cleaned_desc, 'BT', 0.01)}


print("predicted value", basetermResults)
