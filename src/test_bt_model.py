# file used to test model

import pickle
from nltk import word_tokenize
from nltk.stem import PorterStemmer
import numpy as np
import pandas as pd

# load the model from the external file
#ml_model = pickle.load(open('src/model/bt_model.pkl', 'rb'))
ml_model = pickle.load(open('src/model/bt_model.pkl', 'rb'))
# load the vectorizer from the external file
#vectorizer = pickle.load(open("src/model/bt_vectorizer.pkl", "rb"))
vectorizer = pickle.load(open("src/model/bt_vectorizer.pkl", "rb"))

# intialise stemming and stop words
stemming = PorterStemmer()


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
    # tokens = [stemming.stem(w) for w in token_words]
    # Return cleaned text
    return " ".join(tokens)


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
cleaned_desc = [clean_text(description)]
# pre process the inserted list of free text
# cleaned_desc = clean_text_list(description)

####################################################################

# vectorize the cleaned free text using the pre-built TfidfVectorizer (it removes stopwords as well)
test_data_features = vectorizer.transform(cleaned_desc)

print(test_data_features)
# predict the code
'''
probs = ml_model.predict_proba(test_data_features)

# print result
print("inserted text", cleaned_desc)
print("predicted values", sorted(
    zip(ml_model.classes_, probs[0]), key=lambda x: x[1])[-10:])
'''

print("predicted value", ml_model.predict(test_data_features))
