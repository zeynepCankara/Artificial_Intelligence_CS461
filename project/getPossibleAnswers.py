from searchMerriamWebster import searchMerriamWebster
from searchWikipedia import searchWikipedia

def getPossibleAnswers(clue, length):

    wikipediaAnswers = searchWikipedia(clue, length)
    merriamAnswers = searchMerriamWebster(clue, length)

    allAnswers = wikipediaAnswers + merriamAnswers

    return allAnswers