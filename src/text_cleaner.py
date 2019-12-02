# file used to clean the text from an external file and then save it
from collections import Counter
import gensim.parsing.preprocessing as pp
import gensim.utils as utils
import pickle

# load the external file
raw_documents = open('src/dataset/bt_dataset.txt').read().splitlines()

# list in which to save the pre processed lines
ppLines = []

# method used for removing duplicate words from string


def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist


for line in raw_documents:

    # encode the line
    line = utils.any2unicode(line, encoding='utf8', errors='strict')

    # remove stop words
    line = pp.remove_stopwords(line)

    # split numeric values
    line = pp.split_alphanum(line)

    # stem tokens (commented since remove useful info for calculating the cosine distance)
    # line = pp.stem_text(line)

    # strip multiple white spaces
    line = pp.strip_multiple_whitespaces(line)

    # strip only alphanum words (remove strange chars)
    line = pp.strip_non_alphanum(line)

    # strip punctuation
    line = pp.strip_punctuation(line)

    # strip words with length
    line = pp.strip_short(line, minsize=1)

    # remove duplicates
    line = ' '.join(unique_list(line.split()))

    # append the pp line
    ppLines.append(line)

# pickle the file
pickle.dump(dict(enumerate(ppLines)), open("src/dataset/pp_bt_dataset.pkl", "wb"))
