from flask import Flask, request
from flask_cors import CORS

from gensim.similarities import SparseMatrixSimilarity
from gensim.corpora import Dictionary
from gensim.models import TfidfModel

import numpy as np
import pickle

# init Flask and enable Cross Origin Resource Sharing
app = Flask(__name__)
CORS(app)

# load the baseterms
file = open('src/dataset/pp_bt_dataset.pkl', 'rb')
raw_doc = pickle.load(file)

# load the model for the baseterm
index_sparse = SparseMatrixSimilarity.load('src/model/baseterm.index')
print('baseterm model loaded correctly')

# load the dictionary for the baseterm
dictionary = Dictionary.load('src/model/baseterm.dict')
print('baseterm dictionary loaded correctly ', dictionary)

# load tf-idf model fro the baseterm
tf_idf = TfidfModel.load('src/model/baseterm.tfidf')


@app.route("/getSuggestions", methods=['POST'])
def getSuggestions():
    # get the passed json file
    data = request.get_json()

    # if key doesnt exist return none
    baseterm = data['baseterm']
    # facets = data['facets']

    query_doc_bow = dictionary.doc2bow(baseterm)
    print(query_doc_bow)
    query_doc_tf_idf = tf_idf[query_doc_bow]
    print(query_doc_tf_idf)

    # get distance for each sentence in doc (top 10)
    sim = index_sparse[query_doc_tf_idf]
    # save the list of indexes
    indexes = [i[0] for i in sim]

    # get best results
    return ','.join([raw_doc[x] for x in indexes])


if __name__ == "__main__":
    app.run(debug=True)
