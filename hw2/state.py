"""
@Date: 03/03/2021 ~ Version: 2.0
@Groupno: RIDDLER
@Author: Ahmet Feyzi Halaç
@Author: Aybars Altınışık
@Author: Göktuğ Gürbüztürk
@Author: Zeynep Cankara
@Author: Ege Şahin

@Description: Contains the State representation of the puzzle togather with the
beam search routine and puzzle generator to generate distict random puzzles


"""

import copy

# for the beam-search
from collections import deque

# random number generator for the bredth first search
from random import randint

# to try out manhattan distance
import numpy as np


class State(object):
    def __init__(self):
        """State constructor
        Attributes:
            goal_state, type(list): Goal state of the puzzle
            array, type(list): The current state instance
            blank_row, type(int): the empty cell row of the puzzle
            blank_column, type(int): the empty cell column of the puzzle
            size, type(int): the length N of the N x N puzzle grid
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

    # Boundary checks
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

    # Heuristic Function
    def h1(self):
        """ Accumulated distance from the goal state and the array itself"""
        value = np.sum(
            np.abs(np.subtract(
                np.array(self.array), np.array(self.goal_state))))
        return value

    def h2(self):
        """Checks how many numbers in place when compared with the goal state
        The numbers not in place penalised by incrementing the counter by one
        """
        counter = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.array[i][j] != self.goal_state[i][j]:
                    counter = counter + 1
        return counter

    def h(self):
        """Returns the heuristic which penalises the most
        """
        return max(self.h1(), self.h2())

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
    """ Performs beam-search to solve the puzzle. Implements breadth first
    search underneath while the best w nodes selected according to the
    heuristic function. The search ends when the goal state visited. If the
    goal not found and there exist unvisited states the beam-width w increased
    by one and search starts again.
    Params:
        initial_state, typeState): state to start the beam-search routine
        beam_width, type(int): branching factor for the beam-search
    """
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
            next_states = state.get_next()
            # discover the best w candidates
            next_states.sort(key=lambda x: x.h1(), reverse=False)
            next_states = next_states[:min(w, len(next_states))]
            # add the  unvisited children to the queue
            for next_state in next_states:
                if next_state not in visited:
                    queue.append(next_state)

    return path, w


class PuzzleGenerator(object):
    def __init__(self, nof_distinct_states=3, threshold=4):
        """PuzzleGenerator constructor
        Attributes:
            nof_distinct_states, type(int): Number of distinct states to generate
            states, type(set): contains the generated distict states
        Params:
            nof_distinct_states, type(int)
            threshold, type(int): Number of states to generate before selection
        """
        self.nof_distinct_states = nof_distinct_states
        self.threshold = threshold
        self._states = set()
        self.__generate()

    def __shuffle(self, initial_state):
        """Shuffles the given state by making random action selection via
        non-deterministic search routine, starting from the goal state
        Returns:
            initial_state: type(State): State to start shuffling
        """
        count = 0
        queue = deque([initial_state])
        self.visited = set()
        while queue:
            state = queue.popleft()
            self.visited.add(state)
            count += 1
            if(state.is_goal() == False
               and state != initial_state and count > self.threshold):
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

    def __clear(self):
        self._states = set()

    def __generate(self):
        """
        Randomly generates distinct states.
        """
        self.__clear()
        state = State()
        if self.nof_distinct_states > (state.size ** 2-1):
            raise Exception("Error: Number of distinct state size")
        while len(self._states) < self.nof_distinct_states:
            state = self.__shuffle(state)
            if state not in self._states:
                self._states.add(state)

    def get_states(self):
        """Getter for the generated puzzles
        """
        return self._states

    def __str__(self):
        """String representation of the state generator
        Returns:
            type(str), formatted string
        """
        state_no = 1
        puzzle_generator = ""
        for state in self._states:
            puzzle_generator += "\n------ S" + str(state_no) + " ----- \n"
            puzzle_generator += str(state)
            state_no += 1
        return puzzle_generator
