import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


stopWords = set(stopwords.words('english'))

"""This function creates tokens to be searched on the web-sites"""

def getSearchedTokens(clue):

    best_token = clue 
    good_tokens = clue.split('"')[1::2] # find good tokens by searching among quotation marks
    if len(good_tokens) != 0:
        best_token = good_tokens[0]
    
    punctuationFree = clue.translate(str.maketrans('', '', string.punctuation))

    tokens = word_tokenize(punctuationFree)             # split the punctiuation free clue to tokens (list)
    tokens = [w for w in tokens if not w.lower() in stopWords]  # remove stopwordss from tokens

    if best_token not in tokens:
        tokens.append(best_token)

    return [tokens, best_token]