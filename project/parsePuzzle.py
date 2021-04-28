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

def parsePuzzle(debug=False):
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

    if debug:
        return {
            'cells': [{'cellNumber': 1, 'letter': 'P'}, {'cellNumber': 2, 'letter': 'L'}, {'cellNumber': 3, 'letter': 'A'}, {'cellNumber': 4, 'letter': 'N'}, {'cellNumber': 5, 'letter': 'T'}, 
                        {'cellNumber': 6, 'letter': 'H'}, {'cellNumber': 0, 'letter': 'O'}, {'cellNumber': 0, 'letter': 'N'}, {'cellNumber': 0, 'letter': 'O'}, {'cellNumber': 0, 'letter': 'R'}, 
                        {'cellNumber': 7, 'letter': 'I'}, {'cellNumber': 0, 'letter': 'T'}, {'cellNumber': 0, 'letter': 'S'}, {'cellNumber': 0, 'letter': 'M'}, {'cellNumber': 0, 'letter': 'E'},
                        {'cellNumber': 8, 'letter': 'S'}, {'cellNumber': 0, 'letter': 'T'}, {'cellNumber': 0, 'letter': 'E'}, {'cellNumber': 0, 'letter': 'A'}, {'cellNumber': 0, 'letter': 'K'},
                        {'cellNumber': 9, 'letter': 'H'}, {'cellNumber': 0, 'letter': 'O'}, {'cellNumber': 0, 'letter': 'L'}, {'cellNumber': 0, 'letter': 'D'}, {'cellNumber': 0, 'letter': 'S'}],
            'acrossClues': {1: 'Test of responsibility before a pet or kid', 6: 'Word before student or system ', 7: 'First line on the phone to someone you know well', 8: 'Rare order at a restaurant', 9: 'Waits on the phone'},
            'downClues': {1: 'Jam band fronted by guitarist Trey Anastasio', 2: 'Scratch-off ticket game', 3: '"Moon And Half Dome" photographer Adams', 4: 'Wanderer', 5: 'Arduous journeys'}
        }
    driver = webdriver.Chrome(ChromeDriverManager().install())
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

    return {
        'cells': cells,
        'acrossClues': acrossClues,
        'downClues': downClues
    }