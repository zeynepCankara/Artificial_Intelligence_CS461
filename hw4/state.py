"""
@Date: 03/14/2021 ~ Version: 1.0
@Groupno: RIDDLER
@Author: Ahmet Feyzi Halaç
@Author: Aybars Altınışık
@Author: Göktuğ Gürbüztürk
@Author: Zeynep Cankara
@Author: Ege Şahin

@Description: Contains the State representation of the puzzle togather with the
Branch and Bound with Dynamic Programming search routine and puzzle generator to generate distict random puzzles

"""

import copy

# for the queue
from collections import deque

# random number generator for the bredth first search
from random import randint


class State(object):
    def __init__(self):
        """State constructor
        Attributes:
            goal_state, type(list): Goal state of the puzzle
            array, type(list): The current state instance
            blank_row, type(int): the empty cell row of the puzzle
            blank_column, type(int): the empty cell column of the puzzle
            size, type(int): the length N of the N x N puzzle grid
            h_value, type(int): the heuristic value of a state object
        """
        self.goal_state = [[1, 2, 3, 4],
                           [5, 6, 7, 8],
                           [9, 10, 11, 12],
                           [13, 14, 15, 0]]
        self.array = [[1, 2, 3, 4],
                      [5, 6, 7, 8],
                      [9, 10, 11, 12],
                      [13, 14, 15, 0]]
        self.blank_row = 3
        self.blank_column = 3
        self.size = 4
        self.h_value = 0
        self.pos_1 = [[0, 0]]
        self.pos_2 = [[0, 1], [1, 0]]
        self.pos_3 = [[0, 2], [1, 1], [2, 0]]
        self.pos_4 = [[0, 3], [1, 2], [2, 1], [3, 0]]
        self.pos_5 = [[1, 3], [2, 2], [2, 3], [3, 1], [3, 2]]
        self.pos_0 = [[3, 3]]

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
        """Returns an array which the zero tile moved up one time,
        Params:
            inplace, type(bool): modifies the grid in place
        Returns:
            deepcopy or shallowcopy of a state, type(State)
        """
        if self.up_reachable() == False:
            raise Exception("Error: Can't move up!")
        if inplace == False:
            state = copy.deepcopy(self)
        else:
            state = self

        row = state.blank_row - 1
        column = state.blank_column

        state.swap(state.blank_row, state.blank_column, row, column)

        # calculate new h value
        state.h_value = state.h()

        # update the blank space position
        state.blank_row -= 1

        return None if inplace == True else state

    def down(self, inplace=False):
        """Returns an array which the zero tile moved down one time,
        Params:
            inplace, type(bool): modifies the grid in place
        Returns:
            deepcopy or shallowcopy of a state, type(State)
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

        # calculate new h value
        state.h_value = state.h()

        # update the blank space position
        state.blank_row += 1
        return None if inplace == True else state

    def right(self, inplace=False):
        """Returns an array which the zero tile moved right one time,
        Params:
            inplace, type(bool): modifies the grid in place
        Returns:
            deepcopy or shallowcopy of a state, type(State)
        """
        if self.right_reachable() == False:
            raise Exception("Error: Can't move right!")
        if inplace == False:
            state = copy.deepcopy(self)
        else:
            state = self

        row = state.blank_row
        column = state.blank_column + 1

        state.swap(state.blank_row, state.blank_column, row, column)

        # calculate new h value
        state.h_value = state.h()

        # update the blank space position
        state.blank_column += 1
        return None if inplace == True else state

    def left(self, inplace=False):
        """Returns an array which the zero tile moved left one time,
        Params:
            inplace, type(bool): modifies the grid in place
        Returns:
            deepcopy or shallowcopy of a state, type(State)
        """
        if self.left_reachable() == False:
            raise Exception("Error: Can't move left!")
        if inplace == False:
            state = copy.deepcopy(self)
        else:
            state = self

        row = state.blank_row
        column = state.blank_column - 1

        state.swap(state.blank_row, state.blank_column, row, column)

        # calculate new h value
        state.h_value = state.h()

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
    def h(self):
        """ Manhattan distance from the goal state and the array itself"""
        manhattan = 0
        goal_pos = []
        for row in range(self.size):
            for col in range(self.size):
                if self.array[row][col] == 1:
                    goal_pos = self.pos_1
                elif self.array[row][col] == 2:
                    goal_pos = self.pos_2
                elif self.array[row][col] == 3:
                    goal_pos = self.pos_3
                elif self.array[row][col] == 4:
                    goal_pos = self.pos_4
                elif self.array[row][col] == 5:
                    goal_pos = self.pos_5
                else:
                    goal_pos = self.pos_0

                min = 99
                for pos in goal_pos:
                    new_dist = (abs(pos[0] - row) + abs(pos[1] - col))
                    if new_dist < min:
                        min = new_dist

                manhattan = manhattan + min
        return manhattan

    def __str__(self):
        """String representation of the state
        Returns:
            type(str), formatted string
        """
        state_str = ""
        for row in range(self.size):
            for col in range(self.size):
                if col == self.size - 1:
                    state_str += str(self.array[row][col]) + "\t"
                else:
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


def bnb_search(initial_state):
    """ Performs Branch and Bound search with Dynamic Programming to solve the puzzle.
    The search ends when the goal state visited. If the goal not found returns None.
    Params:
        initial_state, typeState): state to start the beam-search routine
    """
    state = initial_state
    visited = set()

    # Priority queue is used to find best candidate path
    queue = PriorityQueue()
    queue.insert([state])
    while queue:
        path = queue.pop()
        state = path[len(path)-1]
        visited.add(state)
        if state.is_goal():
            return path
        next_states = state.get_next()

        # add the  unvisited children to the queue
        for next_state in next_states:
            # if the state is not reached with a lower h. (Dynamic Programming)
            if next_state not in visited:
                new_path = list(path)
                new_path.append(next_state)
                queue.insert(new_path)

    return None


def queue_h(queue):
    total_h = 0
    for state in queue:
        total_h = total_h + state.h_value
    return total_h


class PuzzleGenerator(object):
    def __init__(self, nof_distinct_states=25, threshold=4):
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
        if self.nof_distinct_states > (25):
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


"""A simple PriorityQueue implementation for Branch and Bound search
"""


class PriorityQueue(object):

    def __init__(self):
        """PriorityQueue constructor creates an empty array
        """
        self.queue = []

    def isEmpty(self):
        """Check if the queue is empty
        """
        return len(self.queue) == 0

    def insert(self, data):
        """Insert an element in the queue
        """
        self.queue.append(data)

    def pop(self):
        """Pop an element according to its priority
        """
        try:
            min = 9999
            min_i = 0
            for i in range(len(self.queue)):
                if queue_h(self.queue[i]) < min:
                    min = queue_h(self.queue[i])
                    min_i = i
            item = self.queue[min_i]
            del self.queue[min_i]
            return item
        except IndexError:
            print()
            exit()
