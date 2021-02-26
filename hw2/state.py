import copy

class State(object):
    def __init__(self):
        """State constructor
        Every object of this class keeps a state information
        which can be achieved by a boat action.
        State represents the number of the cannibals and missionaires
        with their locations as "right" or "left".
        Args:
            missionaries_left: type(int), number of missionaries on the left side of the river
            cannibals_left: type(int), number of cannibals on the left side of the river
            action: type(str), direction of the boat heading to ('left' or 'right').
        Attributes:
            current_action: type(string), Information of the location of the boat; "right" or "left"
            boat_size: type(int), Size of the boat
            nof_missionaries: type(int), Total number of missionaries
            nof_cannibals: type(int), Total number of cannibals
            missionaries_left: type(int), Number of missionaries in the left
            cannibals_left: type(int), Number of cannibals in the left
            missionaries_right: type(int), Number of missionaries in the right
            cannibals_right: type(int), Number of cannibals in the right
        """
        self.goal_state = [[1,2,3,4], [2,3,4,3], [3,4,3,2], [4,3,2,0]]
        self.array = [[1,2,3,4], [2,3,4,3], [3,4,3,2], [4,3,2,0]]
        self.blank_row = 3
        self.blank_column = 3
        self.size = 4

    def is_goal(self):
        """Check whether state is a goal state
        Returns:
            type(bool), True if the state is the goal False otherwise
        """
        return self.array == self.goal_state

    def get_next(self):
        """Returns the possible next states from the given state
        Returns:
            next states, type([State]), List of next possible reachable states
        """
        possible_states = []

        up_state = self.up()
        down_state = self.down()
        right_state = self.right()
        left_state = self.left()

        if up_state:
            possible_states.append(up_state)
        if down_state:
            possible_states.append(down_state)
        if right_state:
            possible_states.append(right_state)
        if left_state:
            possible_states.append(left_state)

        return possible_states


    def up(self, change = False):
        if not change:
            state = copy.copy(self)
        else:
            state = self

        row = state.blank_row - 1
        column = state.blank_column

        if row < 0:
            return False

        state.swap(state.blank_row, state.blank_column, row, column)
        return state


    def down(self, change = False):
        if not change:
            state = self.copy()
        else:
            state = self

        row = state.blank_row + 1
        column = state.blank_column

        if row > self.size - 1 :
            return False

        state.swap(state.blank_row, state.blank_column, row, column)
        return state


    def right(self, change = False):
        if not change:
            state = self.copy()
        else:
            state = self

        row = state.blank_row
        column = state.blank_column + 1

        if column > self.size - 1:
            return False

        state.swap(state.blank_row, state.blank_column, row, column)
        return state


    def left(self, change = False):
        if not change:
            state = self.copy()
        else:
            state = self

        row = state.blank_row
        column = state.blank_column - 1

        if column < 0:
            return False

        state.swap(state.blank_row, state.blank_column, row, column)
        return True


    def swap(self, row1, column1, row2, column2):
        temp = self.array[row1][column1]
        self.array[row1][column1] = self.array[row2][column2]
        self.array[row2][column2] = temp


    def manhattan(self):
        distance = 0
        for row in range(self.size):
            for column in range(self.size):
                if self.array[row][column] != 0 and self.array[row][column] != self.goal_state[row][column]:
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
                    return [row,col]
        
        return False


    def in_borders(self, i):
        if i < 0 or i > self.size - 1:
            return False
        else:
            return True 


    def print(self):
        for row in range(self.size):
            for col in range(self.size):
                print(str(self.array[row][col]) + " - ", end =" ")
            print()
        print()


    def copy(self):
        copy = State()
        copy.array = self.array.copy()
        copy.blank_column = self.blank_column
        copy.blank_row = self.blank_row
        copy.goal_state = self.goal_state
        copy.size = self.size

        return copy


    def __str__(self):
        """String representation of the state
        Returns:
            type(str), formatted string
        """
        str = ""
        for row in range(self.size):
            for col in range(self.size):
                str = str + self.array[row][col] + " - "
            str = str + "\n"

        return str


    def __eq__(self, other):
        """Comparison function for states
        Args:
            other: type(State), state to be compared
        Returns:
            type(bool) true if they are equal, false otherwise
        """
        return self.array == other.array


    def __hash__(self):
        """Calculates an hash number from the properties indicated.
        Hash can be used in comparison of two instances.
        Returns:
            type(int) hash number
        """
        return hash(
            (
                self.array
            )
        )