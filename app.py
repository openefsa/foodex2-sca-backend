from flask import Flask, request
from flask_cors import CORS

from nltk import word_tokenize

import pickle as pk

# init Flask and enable Cross Origin Resource Sharing
app = Flask(__name__)
CORS(app)

# load the model from the external file
ml_model = pk.load(open('src/model/bt_model.pkl', 'rb'))
# load the vectorizer from the external file
vectorizer = pk.load(open("src/model/vectorizer.pkl", "rb"))


def clean_text(raw_text):
    # 1) Convert to lower case and Tokenize
    tokens = word_tokenize(raw_text.lower())
    # 2) Keep only words (removes punctuation and numbers)
    tokens = [w for w in tokens if w.isalpha()]
    # 3) Stemming
    # tokens = [stemming.stem(w) for w in token_words]
    # Return cleaned text
    return " ".join(tokens)


@app.route("/getBaseterm", methods=['POST'])
def getBaseterm():
    # get the passed json file
    data = request.get_json()
    # if key doesnt exist return none
    baseterm = data['baseterm']
    # pre process the inserted free text
    cleaned_desc = [clean_text(baseterm)]

    # vectorize the cleaned text with pre-built TfidfVectorizer (removes also stopwords)
    test_data_features = vectorizer.transform(cleaned_desc)

    # predict top best probabilities
    probs = ml_model.predict_proba(test_data_features)

    results = sorted(zip(ml_model.classes_, probs[0]), key=lambda x: x[1])[-10:]

    # return as json
    return results.to_json()

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
