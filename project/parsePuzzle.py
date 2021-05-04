"""
@Date: 25/02/2021 ~ Version: 1.0
@Author: Ahmet Feyzi Halaç
@Author: Aybars Altınışık
@Author: Göktuğ Gürbüztürk
@Author: Zeynep Cankara
@Author: Ege Şahin

@Description: New York Times Mini Crossword Parser

"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from utils import log

def parsePuzzle():
    """This function opens a browser to get current day's mini puzzle information from the New York Times website
    and it parses the website HTML to get a cleaner puzzle format which can be used for our purpose

    Returns:
        path: type(dict) Dictionary which contains the necessary information to construct puzzle
            
        This dictionary has 3 different elements:
            -acrossClues: type(dict) Dictionary which contains all across clues in its values, with the corresponding cell number as a key
            -downClues: type(dict) Dictionary which contains all down clues in its values, with the corresponding cell number as a key
            -cells: type([dict]) An array of dictionaries, each of which represents a cell in the crossword. This represantation contains
                two keys:
                    -cellNumber: type(int) Indicates the number that is at the top left of the cell. If there is no number, it is 0. If cell is black, it is -1.
                    -letter: type(str) Cell's correct letter in the solution of crossword.
    """
 
    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    log('Parsing puzzle from NYTimes Website')

    #Go to New York Times Website
    driver.get('https://www.nytimes.com/crosswords/game/mini')

    #Select 'Play without an account' option
    driver.find_element_by_class_name('StartModal-underlined--3IDBr').click()

    #Click Reveal button
    revealButton = driver.find_element_by_css_selector('button[aria-label="reveal"]')
    revealButton.click()

    #Select Puzzle option
    revealButton.find_element_by_xpath('./../ul/li[3]').click()
    driver.find_element_by_css_selector('button[aria-label="Reveal"]').click()

    cells = []
    #Get all cells
    for cellElement in driver.find_elements_by_css_selector('g[data-group="cells"] g'):
        cell = {}

        if '1oNaD' in cellElement.find_element_by_tag_name('rect').get_attribute('class'):
            #This is a black cell so change its number to -1
            cell['cellNumber'] = -1
            cell['letter'] = ' '
        else: #Not a black cell

            #If it successfully finds the start text, it means there is a number left top corner of the cell
            #So assign this number to cellNumber of cell dictionary
            try:
                cell['cellNumber'] = int(cellElement.find_element_by_css_selector('text[text-anchor="start"]').text)
            except:
                #If it throws error, it means there is no cell number on the top left, so assign 0 to cellNumber
                cell['cellNumber'] = 0
            
            #Get the correct letter of the cell and assign it to letter property of cell dictionary
            cell['letter'] = cellElement.find_element_by_css_selector('text[text-anchor="middle"]').text

        cells.append(cell)

    parentCluelistContainer = driver.find_element_by_class_name('Layout-clueLists--10_Xl')

    acrossClues = {}
    #Get all Across clues
    for acrossClueContainer in parentCluelistContainer.find_elements_by_xpath('div[1]/ol/li'):
        number = int(acrossClueContainer.find_element_by_css_selector('span:first-child').text)
        clue = acrossClueContainer.find_element_by_css_selector('span:last-child').text
        acrossClues[number] = clue

    downClues = {}
    #Get all Down clues
    for downClueContainer in parentCluelistContainer.find_elements_by_xpath('div[2]/ol/li'):
        number = int(downClueContainer.find_element_by_css_selector('span:first-child').text)
        clue = downClueContainer.find_element_by_css_selector('span:last-child').text
        downClues[number] = clue

    answers = {}
    #Get all answers
    for key, value in acrossClues.items():
        for i in range(0, 25):
            if cells[i]['cellNumber'] == key: # Start location of clue is found
                answer = ''
                while True:
                    answer = answer + cells[i]['letter']
                    i = i + 1
                    if i == 25 or cells[i]['cellNumber'] == -1 or i % 5 == 0:
                        break
                answers[str(key) + 'a'] = answer
                break

    for key, value in downClues.items():
        for i in range(0, 25):
            if cells[i]['cellNumber'] == key: # Start location of clue is found
                answer = ''
                while i < 25 and cells[i]['cellNumber'] != -1:
                    answer = answer + cells[i]['letter']
                    i = i + 5
                answers[str(key) + 'd'] = answer
                break

    driver.quit()
    return {
        'cells': cells,
        'acrossClues': acrossClues,
        'downClues': downClues,
        'answers': answers
    }