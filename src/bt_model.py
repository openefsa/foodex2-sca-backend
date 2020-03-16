# file used for create, train, save and test the model

from sklearn.model_selection import train_test_split
import pandas as pd
import pickle as pk
import numpy as np

''' IMPORT DATA '''
# import the dataframe using pandas
df = pd.read_csv('src/data/bt_cleaned_history.csv')
# df = df.sample(frac=0.1)

print(df.shape)

''' DROP NANs '''
# remove rows having nan values
print("shape w/ nan: ", df.shape)
df.dropna(inplace=True)
print("shape w/o nan: ", df.shape)

''' DATA PREPARATION '''
# get feature column
X = df['ENFOODNAME']
# get label column
y = df['BASETERM_NAME_CODE']

#This converts the Y column's values to numbers representing the baseterms
#labelencoder_Y = LabelEncoder()
#y = labelencoder_Y.fit_transform(y)

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
    pk.dump(vectorizer, open("src/model/bt_vectorizer.pkl", "wb"))
    # words in vocabulary
    # vocab = vectorizer.get_feature_names()
    return vectorizer, train_features


# apply bag of words function to training set
vectorizer, train_features = create_bow(X_train)


def train_model(features, label):
    # CNB is an adaptation of the standard multinomial naive Bayes (MNB)
    # it is particularly suited for imbalanced data sets
    # since it uses statistics from the complement of each class to compute the model’s weights

    print("Training the Complement Naive Bayes model...")
    
    from sklearn.naive_bayes import ComplementNB
    ml_model = ComplementNB()
    # ml_model.fit(features, label)
    # partil_fit useful when dataset is too big to fit in memory at once
    ml_model.partial_fit(features, label, classes=np.unique(label))
    # print the model accuracy
    score = ml_model.score(features, label) * 100
    print('CNB Accuracy: %.0f%%'% score)
    '''
    from sklearn.neural_network import MLPClassifier
    ml_model = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
    
    ml_model.fit(features, label)
    '''
    return ml_model


# initialise and fit model
ml_model = train_model(train_features, y_train)

''' SAVE MODEL '''
# save the model on disk
pk.dump(ml_model, open('src/model/bt_model.pkl', 'wb'))

''' TEST MODEL 
# vectorize the test data
test_features = vectorizer.transform(X_test)

# predict the code
predicted_y = ml_model.predict(test_features)
print("predicted values", predicted_y)
correctly_identified_y = predicted_y == y_test
print("correctly identified ", correctly_identified_y)
accuracy = np.mean(correctly_identified_y) * 100
print('Test accuracy: %.0f%%' % accuracy)
'''