"""
@Date: 03/03/2021 ~ Version: 2.0
@Groupno: RIDDLER
@Author: Ahmet Feyzi Halaç
@Author: Aybars Altınışık
@Author: Göktuğ Gürbüztürk
@Author: Zeynep Cankara
@Author: Ege Şahin

@Description: Solving a variant of the 15 puzzles with beam-search.
    ~The variant version has repeated tiles.

### Libraries
Python 3.6 being used for the homework assignment togather with Numpy.
The packages that I used can imported via requirments.txt if pip3 installed.

    pip3 install -r requirements.txt

### Running the program
    python3 main.py

"""
import state
from state import State, PuzzleGenerator, beam_search
import time
import functools


def timeit(func):
    """
    Performs timing experiements on the function execution, prints the result
    Params:
        func: type(function) to evaluate performance
    """
    @functools.wraps(func)
    def func_exec(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        elapsedTime = end_time - start_time
        print('function: {} . Time elapsed: {} ms'.format(
            func.__name__, int(elapsedTime * 1000)))
    return func_exec


@timeit
def get_puzzle_solve_stats(puzzle):
    """Runs the beam-search algorithm and prints the timing statistics
    """
    path, beam_width = beam_search(puzzle)


def print_solution(path, beam_width):
    """Prints the solution path, state by state.
    """
    rowCurrent = 0
    columnCurrent = 0
    rowNext = 0
    columnNext = 0
    for i in range(len(path)):
        currentPuzzle = path[i]
        print(currentPuzzle)
        if i < (len(path) - 1):
            nextPuzzle = path[i + 1]
            for row in range(nextPuzzle.size):
                for column in range(nextPuzzle.size):
                    if currentPuzzle.array[row][column] == 0:
                        rowCurrent = row
                        columnCurrent = column
                    elif nextPuzzle.array[row][column] == 0:
                        rowNext = row
                        columnNext = column

            if rowCurrent > rowNext:
                action = (" "
                          + str(currentPuzzle.array[rowNext][columnNext])
                          + " ---> down \n")
                print(action)
            elif rowCurrent < rowNext:
                action = (" "
                          + str(currentPuzzle.array[rowNext][columnNext])
                          + " ---> up \n")
                print(action)
            elif columnCurrent > columnNext:
                action = (" "
                          + str(currentPuzzle.array[rowNext][columnNext])
                          + " ---> right \n")
                print(action)
            elif columnCurrent < columnNext:
                action = (" "
                          + str(currentPuzzle.array[rowNext][columnNext])
                          + " ---> left \n")
                print(action)
    print("final beam width: ", str(beam_width))


def main():
    """Main body to run the program"""

    initial_state = State()
    state = initial_state
    puzzle_generator = PuzzleGenerator(threshold=2)
    print("Randomly generated distict puzzles")
    print(puzzle_generator)

    # Solve the generated puzzles
    generated_puzzles = puzzle_generator.get_states()
    puzzle_no = 1
    for puzzle in generated_puzzles:
        print("Solve puzzle S:", str(puzzle_no))
        path, beam_width = beam_search(puzzle)
        print_solution(path, beam_width)
        puzzle_no += 1

    return 0


if __name__ == "__main__":
    main()
