from searchMerriamWebster import searchMerriamWebster
from searchWikipedia import searchWikipedia
from searchWordnet import searchWordnet

def getPossibleAnswers(clue, length):

    wikipediaAnswers = searchWikipedia(clue, length)    # get answers of wikipedia
    merriamAnswers = searchMerriamWebster(clue, length) # get answers of merriam webster
    wordnetAnswers = searchWordnet(clue, length)        # get wordnet answers
    
    allAnswers = wikipediaAnswers + merriamAnswers + wordnetAnswers # merge all answer lists

    return allAnswers