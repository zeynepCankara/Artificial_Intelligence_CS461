"""
@Date: 26/02/2021 ~ Version: 1.0
@Author: Ahmet Feyzi Halaç
@Author: Aybars Altınışık
@Author: Göktuğ Gürbüztürk
@Author: Zeynep Cankara
@Author: Ege Şahin

@Description: Solving a variant of the 15 puzzles with beam-search.
    - The variant version has repeated tiles.

"""
import state
from state import State, PuzzleGenerator, beam_search
import time
import functools


def find_action_sequence(path):
    """Formatted print the visited paths
    TODO: Just show the paths visited  which leads to the goal
    """
    if len(path) <= 0:
        raise Exception("Error: No action transition happened!")
    prev_state = path[0]
    action_sequence = []
    for i in range(1, len(path)):
        current_state = path[i]
        blank_row_prev = prev_state.blank_row
        blank_col_prev = prev_state.blank_column
        blank_row_curr = current_state.blank_row
        blank_col_curr = current_state.blank_column

        if blank_row_prev > blank_row_curr:
            action = (" "
                      + str(current_state.array[blank_row_prev][blank_col_prev])
                      + " -> up \n")
        elif blank_row_prev < blank_row_curr:
            action = (" "
                      + str(current_state.array[blank_row_prev][blank_col_prev])
                      + " -> down \n")
        elif blank_col_prev > blank_col_curr:
            action = (" "
                      + str(current_state.array[blank_row_prev][blank_col_prev])
                      + " -> right \n")
        elif blank_col_prev < blank_col_curr:
            action = (" "
                      + str(current_state.array[blank_row_prev][blank_col_prev])
                      + " -> left \n")
        action_sequence.append(str(prev_state))
        action_sequence.append(action)
        prev_state = current_state
    action_sequence.append(str(prev_state))
    return "".join(action_sequence)


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
    rowCurrent = 0
    columnCurrent = 0
    rowNext = 0
    columnNext = 0
    for i in range(len(path)):
        currentPuzzle = path[i]
        print(path[i])
        if i < (len(path) - 1):
            nextPuzzle = path[i + 1]
            while rowCurrent < 4:
                while columnCurrent < 4:
                    if currentPuzzle.array[rowCurrent][columnCurrent] == 0:
                        break
                    columnCurrent += 1
                rowCurrent += 1    
        
            while rowNext < 4:
                while columnNext < 4:
                    if nextPuzzle.array[rowNext][columnNext] == 0:
                        break
                    columnNext += 1
                rowNext += 1

            if rowCurrent > rowNext:
                action = (" "
                        + str(rowCurrent - rowNext)
                        + " -> down \n")
                print (action)         
            elif rowCurrent < rowNext:
                action = (" "
                        + str(rowNext - rowCurrent)
                        + " -> up \n")
                print(action)         
            elif columnCurrent > columnNext:
                action = (" "
                        + str(columnCurrent - columnNext)
                        + " -> left \n")
                print(action)         
            elif columnCurrent < columnNext:
                action = (" "
                        + str(columnNext - columnCurrent)
                        + " -> right \n")
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
        # print(find_action_sequence(path))
        puzzle_no += 1

    return 0


if __name__ == "__main__":
    main()
