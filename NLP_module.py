
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from PyDictionary import PyDictionary
import pandas as pd
import re
import pickle

def remove_stopwords(sentence):
    '''
    sentence: list of strings
    '''
    sentence=[word.lower() for word in sentence if word not in stop_words]

    return sentence

def lemma(word):
    '''
    :param word: string
    :return: lemmatized string
    '''
    word=wordnet_lemmatizer.lemmatize(word)
    return word

def root(word):
    '''

    :param word: string
    :return: string
     for a string ground that string to a 'root' word.
     so that all synonyms get mapped to the same word
    '''
    word=lemma(word)

    if word in syn_dict.keys():
        return syn_dict[word]
    else:
        if word in syn_dict.values():
            #syn_dict[word]=word
            return word
        else:
            synonyms = dictionary.synonym(word)
            if synonyms!=None:
                syn_dict[synonyms[0]]=word
                return synonyms[0]
            else:
                syn_dict[word]=word
                return word



def ground_words(sentence):
    '''

    :param sentence: string representing multiple words
    :return: string
    takes a sentence and processes it, returning the sentence
    minus the stop words and with words replaed by their lemmas
    and a grounded synonym
    '''
    try:
        sentence=re.findall(r"[\w']+", sentence)
        sentence=remove_stopwords(sentence)
        sentence=[root(word) for word in sentence]
        sentence=' '.join(sentence)
    except:
        sentence=sentence
    return sentence



stop_words = stopwords.words('english')  # upload a dictionary of stopwords, common words like 'and'
wordnet_lemmatizer = WordNetLemmatizer()  # there are other options, but as the language quality does not matter we will stick with what is readily available
dictionary = PyDictionary()  # using the python dictionary to generate synonyms. Can do better maybe

syn_dict={}

data='../repos/'
dUK=pickle.load(open(data+'dUK.pkl','rb'))


pUK=pd.DataFrame.from_dict(dUK,orient='index')

pUK['SM']=pUK['SM'].apply(ground_words)

pUK.to_pickle(data+'pUK.pkl')

pUK['LD']=pUK['LD'].apply(ground_words)


pUK.to_pickle(data+'pUK.pkl')
