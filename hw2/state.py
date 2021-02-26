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
        self.array = [[1,2,3,4], [2,3,4,3], [3,4,3,2], [4,3,2,0]]

    def is_goal(self):
        """Check whether state is a goal state
        Returns:
            type(bool), True if the state is the goal False otherwise
        """
        goal = [[1,2,3,4], [2,3,4,3], [3,4,3,2], [4,3,2,0]]
        return self.array == goal

    def get_next(self):
        """Returns the possible next states from the given state
        Returns:
            next states, type([State]), List of next possible reachable states
        """
        possible_states = []
        action = (
            "right" if self.current_action == "left" else "left"
        )  # Next Action is the reverse of current action
        """
            According to the value of action, these if-else and nested for loops try each possible combination of missionaries and
            cannibals and create a new state. If this state is reacbale it is appended to the possible_state.
        """
        if action == "left":
            for nof_passangers in range(1, self.boat_size + 1):
                for nof_cannibal_passengers in range(0, nof_passangers + 1):
                    nof_missionary_passengers = nof_passangers - nof_cannibal_passengers
                    new_state = State(
                        self.missionaries_left - nof_missionary_passengers,
                        self.cannibals_left - nof_cannibal_passengers,
                        action,
                    )
                    if new_state.is_reachable():
                        possible_states.append(new_state)

        else:
            for nof_passangers in range(1, self.boat_size + 1):
                for nof_cannibal_passengers in range(0, nof_passangers + 1):
                    nof_missionary_passengers = nof_passangers - nof_cannibal_passengers
                    new_state = State(
                        self.missionaries_left + nof_missionary_passengers,
                        self.cannibals_left + nof_cannibal_passengers,
                        action,
                    )
                    if new_state.is_reachable():
                        possible_states.append(new_state)
        return possible_states

    def __str__(self):
        """String representation of the state
        Returns:
            type(str), formatted string
        """

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