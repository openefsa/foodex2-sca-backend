# file used for create, train, save and test the model

from sklearn.model_selection import train_test_split
import pandas as pd
import pickle as pk
import numpy as np

''' IMPORT DATA '''
# import the dataframe using pandas
df = pd.read_csv('src/data/FoodEx2_History_Facets.csv')

''' DROP NANs '''
# remove rows having nan values
print("shape w/ nan: ", df.shape)
df = df.fillna('')
print("shape w/o nan: ", df.shape)

# use 50% of the whole dataframe (random_state=1 used for reproducing the same sample)
df = df.sample(frac=0.05)

''' DATA PREPARATION '''
# get feature column
X = df['BASETERM_NAME']
# get label column
y = df.drop('BASETERM_NAME', axis=1)
# split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01)


def create_bow(X):
    # create bag of words for the given series
    print('Creating bag of words...')
    from sklearn.feature_extraction.text import TfidfVectorizer
    # Initialize the TfidfVectorizer
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), use_idf=True)
    # fit the model and transform training data into feature vectors
    # (convert to a NumPy array for easy handling)
    train_features = vectorizer.fit_transform(X)
    # pickle the vocabulary
    pk.dump(vectorizer, open("src/model/vectorizer.pkl", "wb"))
    # words in vocabulary
    # vocab = vectorizer.get_feature_names()
    return vectorizer, train_features


# apply bag of words function to training set
vectorizer, train_features = create_bow(X_train)


def train_model(features, label):
    
    print("Training the Complement Naive Bayes model...")
    # CNB is an adaptation of the standard multinomial naive Bayes (MNB)
    # it is particularly suited for imbalanced data sets
    # since it uses statistics from the complement of each class to compute the model’s weights
    from sklearn.multioutput import MultiOutputClassifier
    from sklearn.neighbors import KNeighborsClassifier
    ml_model = MultiOutputClassifier(KNeighborsClassifier())
    ml_model.fit(features, label)
    # partil_fit useful when dataset is too big to fit in memory at once
    #ml_model.partial_fit(features, label, classes=np.unique(label))
    # print the model accuracy
    score = ml_model.score(features, label) * 100
    print('CNB Accuracy: %.0f%%' % score)

    return ml_model


# initialise and fit model
ml_model = train_model(train_features, y_train)

''' SAVE MODEL '''
# save the model on disk
pk.dump(ml_model, open('src/model/fc_model.pkl', 'wb'))

''' TEST MODEL '''
# vectorize the test data
''' TEST MODEL '''
# vectorize the test data
test_features = vectorizer.transform(["white chocolate with hazelnuts"])

## predict the code
predicted_y = ml_model.predict(test_features)

# print result
print("predicted values", predicted_y)


## predict the code
predicted_y = ml_model.predict(test_features)

# print result
print("predicted values", predicted_y)
