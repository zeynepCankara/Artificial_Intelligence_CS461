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
from state import State, PuzzleGenerator


def main():
    """Main body to run the program"""

    print()
    initial_state = State()
    goal_state = [[1, 2, 3, 4],
                  [2, 3, 4, 3],
                  [3, 4, 3, 2],
                  [4, 3, 2, 0]]
    state = initial_state
    puzzle_generator = PuzzleGenerator()
    puzzles = puzzle_generator.generate(3)
    for puzzle in puzzles:
        print(puzzle)
    """
    print(initial_state.array == goal_state)
    a = initial_state.get_next()
    queue = []
    for b in a:
        b_next = b.get_next()
        """


if __name__ == "__main__":
    main()
