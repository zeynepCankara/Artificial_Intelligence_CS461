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
import copy
import state
from state import State, PuzzleGenerator, beam_search


def main():
    """Main body to run the program"""

    initial_state = State()
    state = initial_state
    puzzle_generator = PuzzleGenerator()

    path, w_final = beam_search(list(puzzle_generator.states)[0])
    for puzzle in path:
        print(puzzle)
        print("h val: ", puzzle.h())
    print(w_final)

    """
    print(initial_state.array == goal_state)
    a = initial_state.get_next()
    queue = []
    for b in a:
        b_next = b.get_next()
        """


if __name__ == "__main__":
    main()
