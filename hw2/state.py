import copy

# for the breadth-first-search
from collections import deque

# random number generator for the bredth first search
from random import randint

# to try out manhattan distance
import numpy as np


class State(object):
    def __init__(self):
        """State constructor
        """
        self.goal_state = [[1, 2, 3, 4],
                           [2, 3, 4, 3],
                           [3, 4, 3, 2],
                           [4, 3, 2, 0]]
        self.array = [[1, 2, 3, 4],
                      [2, 3, 4, 3],
                      [3, 4, 3, 2],
                      [4, 3, 2, 0]]
        self.blank_row = 3
        self.blank_column = 3
        self.size = 4

    def is_goal(self):
        """Check whether state is a goal state
        Returns:
            type(bool), True if the state is the goal False otherwise
        """
        return self.array == self.goal_state

    def down_reachable(self):
        return self.blank_row < self.size - 1

    def up_reachable(self):
        return self.blank_row > 0

    def left_reachable(self):
        return self.blank_column > 0

    def right_reachable(self):
        return self.blank_column < self.size - 1

    def get_next(self):
        """Returns the possible next states from the given state
        Returns:
            next states, type([State]), List of next possible reachable states
        """
        possible_states = []

        if self.up_reachable() == True:
            possible_states.append(self.up())
        if self.down_reachable() == True:
            possible_states.append(self.down())
        if self.right_reachable() == True:
            possible_states.append(self.right())
        if self.left_reachable() == True:
            possible_states.append(self.left())

        return possible_states

    def up(self, inplace=False):
        if self.up_reachable() == False:
            raise Exception("Error: Can't move up!")
        if inplace == False:
            state = copy.deepcopy(self)
        else:
            state = self

        row = state.blank_row - 1
        column = state.blank_column

        state.swap(state.blank_row, state.blank_column, row, column)
        # update the blank space position
        state.blank_row -= 1

        return None if inplace == True else state

    def down(self, inplace=False):
        """
        Move down action
        Params: inplace, type(bool): modifies the grid in place
        """
        if self.down_reachable() == False:
            raise Exception("Error: Can't move down!")
        if inplace == False:
            state = copy.deepcopy(self)
        else:
            state = self

        row = state.blank_row + 1
        column = state.blank_column

        state.swap(state.blank_row, state.blank_column, row, column)
        # update the blank space position
        state.blank_row += 1
        return None if inplace == True else state

    def right(self, inplace=False):
        if self.right_reachable() == False:
            raise Exception("Error: Can't move right!")
        if inplace == False:
            state = copy.deepcopy(self)
        else:
            state = self

        row = state.blank_row
        column = state.blank_column + 1

        state.swap(state.blank_row, state.blank_column, row, column)
        # update the blank space position
        state.blank_column += 1
        return None if inplace == True else state

    def left(self, inplace=False):
        if self.left_reachable() == False:
            raise Exception("Error: Can't move left!")
        if inplace == False:
            state = copy.deepcopy(self)
        else:
            state = self

        row = state.blank_row
        column = state.blank_column - 1

        state.swap(state.blank_row, state.blank_column, row, column)
        # update the blank space position
        state.blank_column -= 1
        return None if inplace == True else state

    def swap(self, row1, column1, row2, column2):
        """ Swaps two positions in the grid
        """
        temp = self.array[row1][column1]
        self.array[row1][column1] = self.array[row2][column2]
        self.array[row2][column2] = temp

    def h(self):
        """ Manhattan distance from the goal state and the array itself"""
        return np.sum(np.abs(np.array(self.array), np.array(self.goal_state)))

    def __str__(self):
        """String representation of the state
        Returns:
            type(str), formatted string
        """
        state_str = ""
        for row in range(self.size):
            for col in range(self.size):
                state_str += str(self.array[row][col]) + " - "
            state_str += "\n"

        return state_str

    def __eq__(self, other):
        """Comparison function for states
        Args:
            other: type(State), state to be compared
        Returns:
            type(bool) true if they are equal, false otherwise
        """
        return str(self.array) == str(other.array)

    def __hash__(self):
        """Calculates an hash number from the properties indicated.
        Hash can be used in comparison of two instances.
        Returns:
            type(int) hash number
        """
        return hash(str(self.array))


def beam_search(initial_state, beam_width=2):
    w = beam_width-1
    state = initial_state
    while state.is_goal() == False:
        w += 1
        path = []
        visited = set()
        queue = deque([state])
        while queue:
            state = queue.popleft()
            visited.add(state)
            path.append(copy.copy(state))
            if state.is_goal():
                return path, w
            states = state.get_next()
            # discover the best w candidates
            states.sort(key=lambda x: x.h(), reverse=True)
            states = states[:min(w, len(states))]
            for next_state in states:
                if next_state not in visited:
                    queue.append(next_state)

    return path, w


class PuzzleGenerator(object):
    def __init__(self, nof_distinct_states=3):
        """PuzzleGenerator constructor
        Attributes:
        """
        self.nof_distinct_states = nof_distinct_states
        self.states = set()
        self.generate()

    def shuffle(self, state):
        """Shuffles the given state by making random action selection
        Returns:
            state: type(State) shuffled state
        """
        initial_state = state
        queue = deque([state])
        self.visited = set()
        while queue:
            state = queue.popleft()
            self.visited.add(state)
            if state.is_goal() == False and state != initial_state:
                return state
            states = state.get_next()
            for next_state in states:
                if next_state not in self.visited:
                    # random selection of next states
                    random_idx = randint(0, len(queue))
                    # insert to queue randomly
                    if random_idx < len(queue):
                        queue.insert(random_idx, next_state)
                    else:
                        queue.append(next_state)

    def clear(self):
        self.states = set()

    def generate(self):
        """
        Randomly generates 3 distinct states.
        Returns:
            type(tuple(State)), 3 distinct states
        """
        self.clear()
        state = State()
        if self.nof_distinct_states > (state.size ** 2-1):
            raise Exception("Error: Number of distinct state size")
        while len(self.states) < self.nof_distinct_states:
            state = self.shuffle(state)
            if state not in self.states:
                self.states.add(state)
        return self.states

    def __str__(self):
        """String representation of the state generator
        Returns:
            type(str), formatted string
        """
        state_no = 1
        puzzle_generator = ""
        for state in self.states:
            puzzle_generator += "\n------ S" + str(state_no) + " ----- \n"
            puzzle_generator += str(state)
            state_no += 1
        return puzzle_generator
