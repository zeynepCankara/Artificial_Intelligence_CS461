import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


stopWords = set(stopwords.words('english'))

"""This function creates tokens to be searched on the web-sites"""

def getSearchedTokens(clue):

    best_token = clue
    good_tokens = clue.split('"')[1::2]
    if len(good_tokens) != 0:
        best_token = good_tokens[0]
    
    punctuationFree = clue.translate(str.maketrans('', '', string.punctuation))

    tokens = word_tokenize(punctuationFree)             # split the punctiuation free clue to tokens (list)
    tokens = [w for w in tokens if not w in stopWords]  # remove stopwordss from tokens

    tokenNum = len(tokens)

    max = 0

    for i in range(tokenNum):
        new_token = tokens[i]
        for j in range(i+1,tokenNum):
            new_token = new_token + " " + tokens[j]
            tokens.append(new_token)
            if len(new_token) > max and len(good_tokens) == 0:
                max = len(new_token)
                best_token = new_token

    if best_token not in tokens:
        tokens.append(best_token)

    return [tokens, best_token]