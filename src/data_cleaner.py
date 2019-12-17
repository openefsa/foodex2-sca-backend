# this file is used for cleaning a dataset retrived from a csv file

import pandas as pd
import string


''' IMPORT DATA '''
# import the dataframe using pandas
df = pd.read_csv('src/data/history_4.csv', low_memory=False)

''' LOWER CASE '''
df['ENFOODNAME'] = df['ENFOODNAME'].str.lower()
# df = df.apply(lambda x: x.astype(str).str.lower())

''' REMOVE PUNCTATION '''


def remove_punctuation(text):
    # replace punctation with single space
    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
    # return the text with no punctation marks
    return text.translate(translator)


# remove punctation from term name and term warning
df['ENFOODNAME'] = df['ENFOODNAME'].apply(remove_punctuation)

''' TRIM MULTI-SPACES '''
# replace single chars with space
# df['ENFOODNAME'].replace( {'\\s\\D\\s': ' '}, regex=True, inplace=True)

# replace multiple white spaces with single one
df.replace({' +': ' '}, regex=True, inplace=True)


''' STEMMING 
# create an object of stemming function
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")

def stemming(text):
    # function that stem each word given a text
    text = [stemmer.stem(word) for word in text.split()]
    return " ".join(text)

# apply stemming to specified columns
df['ENFOODNAME'] = df['ENFOODNAME'].apply(stemming)
'''

''' EXPORT THE DATAFRAME '''
# export the df cleaned
export_csv = df.to_csv(r'src/data/cleaned_history_4.csv', index=None)
