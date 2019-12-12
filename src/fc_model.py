import gensim.utils as utils

from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.similarities import SparseMatrixSimilarity

import pandas as pd

# load the external file
df = pd.read_pickle('src/dataset/bt_cleaned.pkl')

# tokenize each sentence using nltk
gen_docs = [[w.lower() for w in utils.tokenize(text)]
            for text in df]

# build gensim dictionary (map word to number)
dictionary = Dictionary(gen_docs)
# save dictionary in disk
dictionary.save('./src/model/baseterm.dict')

'''
print(dictionary[5])
print(dictionary.token2id['teff'])
print("Number of words in dictionary:", len(dictionary))
for i in range(len(dictionary)):
    print(i, dictionary[i])
'''

# buld the corpus, list of bow (no of time appears in doc)
corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
# print(corpus)

# create the tf-idf model from corpus
tf_idf = TfidfModel(corpus)
# save tf-idf model
tf_idf.save('./src/model/baseterm.tfidf')

# create similarity measure in tf-idf space
index_sparse = SparseMatrixSimilarity(
    tf_idf[corpus], num_features=len(dictionary), num_best=10)

# print(sims)
# print(type(sims))

# save model to disk
index_sparse.save('./src/model/baseterm.index')
