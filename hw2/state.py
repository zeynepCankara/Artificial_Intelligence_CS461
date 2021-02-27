import copy

# for the breadth-first-search
from collections import deque

# random number generator for the bredth first search
from random import randint


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
            raise Exception("Error: Can't right down!")
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
            raise Exception("Error: Can't left down!")
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

    def manhattan(self):
        distance = 0
        for row in range(self.size):
            for column in range(self.size):
                if (self.array[row][column] != 0
                        and self.array[row][column] != self.goal_state[row][column]):
                    index = self.find(row, column, self.array[row][column])
                    distance += abs(row-index[0]) + abs(column-index[1])

        return distance

    def find(self, row, col, item):
        distance = 1
        found = False
        while not found and distance < self.size:
            found = self.check_surroundings(distance, row, col, item)
            if found:
                return found

        return False

    def check_surroundings(self, distance, row, col, item):
        rows = []
        cols = []

        new_row = row + distance
        if self.in_borders(new_row):
            rows.append(new_row)

        new_row = row - distance
        if self.in_borders(new_row):
            rows.append(new_row)

        new_col = col + distance
        if self.in_borders(new_col):
            cols.append(new_col)

        new_col = col - distance
        if self.in_borders(new_col):
            cols.append(new_col)

        for row in rows:
            for col in cols:
                if self.goal_state[row][col] == item:
                    return [row, col]

        return False

    def in_borders(self, i):
        if i < 0 or i > self.size - 1:
            return False
        else:
            return True

    def print(self):
        for row in range(self.size):
            for col in range(self.size):
                print(str(self.array[row][col]) + " - ", end=" ")
            print()
        print()

    def beam_search(self, w):
        # TODO complete
        if self.is_goal():
            return self
        if w == 0:
            return False
        counter = w
        candidates = []
        possible_states = self.get_next()

        for state in possible_states:
            if counter == 0:
                max = 0
                heuristic = state.manhattan()
                for candidate in candidates:
                    if candidate.manhattan() > max:
                        max = candidate.manhattan()
                        max_state = candidate
                if heuristic < max:
                    candidates.remove(candidate)
                    candidates.append(state)
            else:
                candidates.append(state)

        for candidate in candidates:
            return candidate.beam_search(w)

    def shuffle(self):
        # TODO
        self.up()
        self.left()
        self.left()
        self.down()
        self.right()
        self.up()
        self.up()
        self.right()

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


class PuzzleGenerator(object):
    def __init__(self):
        """PuzzleGenerator constructor
        Attributes:
        """
        self.puzzles = set()
        self.actions = {1: "left", 2: "down", 3: "right", 4: "down"}

    def shuffle(self, state):
        """Shuffles the given state
        Returns:
            state: type(State) shuffled state
        """
        queue = deque([state])
        self.visited = set()
        initial_state = state
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

    def generate(self):
        """
        Randomly generates 3 distinct states.
        Returns:
            type(tuple(State)), 3 distinct states
        """
        state = State()
        while len(self.puzzles) < 3:
            print(state)
            state = self.shuffle(state)
            if state not in self.puzzles:
                self.puzzles.add(state)
        return self.puzzles
