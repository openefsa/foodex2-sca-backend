# this file is used for cleaning a dataset retrived from a csv file

import pandas as pd
import string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

""" IMPORT DATA """
# import the dataframe using pandas
df = pd.read_csv("src/data/bt_data_model.csv")

""" LOWER CASE """
df["ENFOODNAME"] = df["ENFOODNAME"].str.lower()
# df['BT_ONLY_EXPLICIT'] = df['BT_ONLY_EXPLICIT'].str.lower()
# df = df.apply(lambda x: x.astype(str).str.lower())
df["ENFOODNAME"] = df["ENFOODNAME"].fillna("")
# df['BT_ONLY_EXPLICIT'] = df['BT_ONLY_EXPLICIT'].fillna('')
df["BASETERM_NAME_CODE"] = df["BASETERM_NAME_CODE"].fillna("")


""" REMOVE STOP WORDS """


def remove_stop_words(s):
    # set the english stop words list
    en_stops = set(stopwords.words("english"))
    # split the given input (using nltk)
    tokens = word_tokenize(s)
    # keep only non-stop-words
    filtered_sentence = [w for w in tokens if not w in en_stops]
    # return string
    return " ".join(filtered_sentence)


# remove stop words
df["ENFOODNAME"] = df["ENFOODNAME"].apply(remove_stop_words)
# df['BT_ONLY_EXPLICIT'] = df['BT_ONLY_EXPLICIT'].apply(remove_stop_words)

""" REMOVE PUNCTATION """


def remove_punctuation(text):
    # replace punctation with single space
    translator = str.maketrans(string.punctuation, " " * len(string.punctuation))
    # return the text with no punctation marks
    return text.translate(translator)


# remove punctation from term name and term warning
df["ENFOODNAME"] = df["ENFOODNAME"].apply(remove_punctuation)
# df['BT_ONLY_EXPLICIT'] = df['BT_ONLY_EXPLICIT'].apply(remove_punctuation)

""" TRIM MULTI-SPACES """
# replace single chars with space
# df['ENFOODNAME'].replace( {'\\s\\D\\s': ' '}, regex=True, inplace=True)

# replace multiple white spaces with single one
df.replace({" +": " "}, regex=True, inplace=True)


""" STEMMING """
# create an object of stemming function
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("english")


def stemming(text):
    # function that stem each word given a text
    text = [stemmer.stem(word) for word in text.split()]
    return " ".join(text)


# apply stemming to specified columns
df["ENFOODNAME"] = df["ENFOODNAME"].apply(stemming)

""" EXPORT THE DATAFRAME """
# export the df cleaned
export_csv = df.to_csv(r"src/data/bt_cleaned_history.csv", index=None)
