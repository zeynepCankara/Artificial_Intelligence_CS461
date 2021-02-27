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


def print_solution(path):
    for puzzle in path:
        print(puzzle)
        print("h val: ", puzzle.h())


def main():
    """Main body to run the program"""

    initial_state = State()
    state = initial_state
    puzzle_generator = PuzzleGenerator()
    # Solve the generated puzzles
    for puzzle in puzzle_generator.states:
        print("Start beam search routine")
        path, beam_width = beam_search(puzzle)
        print_solution(path)
        print("Final beam width: ", beam_width)


if __name__ == "__main__":
    main()
