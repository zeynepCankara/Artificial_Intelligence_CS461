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


def find_action_sequence(path):
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


def print_solution(path):
    for puzzle in path:
        print(puzzle)
        print("h val: ", puzzle.h())


def main():
    """Main body to run the program"""

    initial_state = State()
    state = initial_state
    puzzle_generator = PuzzleGenerator()
    for puzzle in puzzle_generator.states:
        print("puzzle")
        print(puzzle)
        # print(puzzle.h())

    # Solve the generated puzzles

    for puzzle in puzzle_generator.states:
        print("Start beam search routine")
        path, beam_width = beam_search(puzzle)
        # print(find_action_sequence(path))
        print_solution(path)
        print("Final beam width: ", beam_width)

    return 0


if __name__ == "__main__":
    main()
