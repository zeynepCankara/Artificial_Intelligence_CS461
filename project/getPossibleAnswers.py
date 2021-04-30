from searchMerriamWebster import searchMerriamWebster
from searchWikipedia import searchWikipedia
from searchWordnet import searchWordnet

def getPossibleAnswers(clue, length):

    wikipediaAnswers = searchWikipedia(clue, length)
    merriamAnswers = searchMerriamWebster(clue, length)
    wordnetAnswers = searchWordnet(clue, length)
    
    allAnswers = wikipediaAnswers + merriamAnswers + wordnetAnswers

    return allAnswers