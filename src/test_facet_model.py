# file used to test model

import pickle
from nltk import word_tokenize
from nltk.stem import PorterStemmer
import numpy as np
import pandas as pd

# load the model from the external file
fc_model = pickle.load(open("src/model/fc_model.pkl", "rb"))
# load the vectorizer from the external file
vectorizer = pickle.load(open("src/model/fc_vectorizer.pkl", "rb"))

# intialise stemming and stop words
# stemming = PorterStemmer()


def clean_text_list(X):
    # method for text cleaning list of raw data
    cleaned_X = []
    for element in X:
        cleaned_X.append(clean_text(element))
    return cleaned_X


def clean_text(raw_text):
    # 1) Convert to lower case and Tokenize
    tokens = word_tokenize(raw_text.lower())
    # 2) Keep only words (removes punctuation and numbers)
    tokens = [w for w in tokens if w.isalpha()]
    # 3) Stemming
    # tokens = [stemming.stem(w) for w in tokens]

    return " ".join(tokens)


# free text food description (english)
"""
description = ["oat",
               "strawberry flavour milk",
               "chocolate with cow milk semi skimed and sterlised",
               "apple pie",
               "pie with apples",
               "white chocolate with hazelnuts"]
"""
description = "white chocolate with coconut flakes"
# description = "pizza with spinach"

# pre process the inserted free text
d = clean_text(description)
cleaned_desc = ["A034P:" + d]
print(cleaned_desc)
# pre process the inserted list of free text
# cleaned_desc = clean_text_list(description)

####################################################################

# vectorize the cleaned free text using the pre-built TfidfVectorizer (it removes stopwords as well)
test_data_features = vectorizer.transform(cleaned_desc)

print(test_data_features)

# predict top best probabilities
probs = fc_model.predict_proba(test_data_features)
# zip target class to affinity
results = zip(fc_model.classes_, probs[0])
# sort descending and get top 10
results = sorted(results, key=lambda x: x[1], reverse=True)[:10]
print(results)

'''
# create the list of facets without affinity (not useful at the moment)
lst = []
for item in results:
    lst.append(item[0].split(";"))
# create the df from the list of list
df = pd.DataFrame(lst)
# rename the headers of df
df.columns = [
    "F01",
    "F02",
    "F03",
    "F04",
    "F06",
    "F07",
    "F08",
    "F09",
    "F10",
    "F11",
    "F12",
    "F17",
    "F18",
    "F19",
    "F20",
    "F21",
    "F22",
    "F23",
    "F24",
    "F25",
    "F26",
    "F27",
    "F28",
    "F29",
    "F30",
    "F31",
    "F32",
    "F33"
]
items = dict()
# for each column get the unqieue values for the specific facet group
for col in df:
    cl = df.loc[:, col].unique()
    for i, x in enumerate(cl):
        if x != "N.A.":
            facets = x.split("$")
            ls = []
            for facet in facets:
                fc_info = facet.split(":")
                ls.append({"code": fc_info[0], "name": fc_info[1]})
            items[col] =ls

print(items)
'''

"""

print("predicted value", ml_model.predict(test_data_features))
"""

