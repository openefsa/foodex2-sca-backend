# Import all the dependencies
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize

import logging
logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


raw_documents = open('./src/dataset/bt_dataset.txt').read().splitlines()
tokenized_sents = [[w.lower() for w in word_tokenize(text)]
            for text in raw_documents]

sentences = [TaggedDocument((doc), [i]) for i, doc in enumerate(tokenized_sents)]

model = Doc2Vec(vector_size=5, window=2, dm=0, dbow_words=1, workers=4)

model.build_vocab(sentences)

for epoch in range(100):
    print('iteration {0}'.format(epoch))
    model.train(sentences, total_examples=model.corpus_count,
                epochs=model.epochs)
    model.alpha -= 0.0025  # decrease the learning rate
    model.min_alpha = model.alpha  # fix the learning rate, no decay

model.save("./src/model/d2v.model")
print("Model Saved")
