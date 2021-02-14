"""
@Date: 13/02/2021 ~ Version: 1.0
@Authors:...

@Description: A version of the missionaries and cannibals problem.
              ~ Non-deterministic search
"""

# data science related
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# queue for the nondeterministic search
from collections import deque

# random number generator for the nondeterministic search
from random import randint


class State(object):
    def __init__(self, missionaries_left, cannibals_left, action = None):
        self.current_action = action
        self.boat_size = 5
        self.nof_missionaries = 6
        self.nof_cannibals = 6
        self.missionaries_left = missionaries_left
        self.cannibals_left = cannibals_left
        self.missionaries_right = self.nof_missionaries - missionaries_left
        self.cannibals_right = self.nof_cannibals - cannibals_left

    def is_goal(self):
        """Check whether state is a goal state
        Returns:
            type(bool), True if the state is the goal False otherwise
        """
        return self.missionaries_left == 0 and self.cannibals_left == 0

    def is_reachable(self):
        """Check whether the state is reachable by checking the conditions
        Returns:
            type(bool), True if the state is reachable False otherwise
        """

        # condition on number of missionaries and cannibals
        if (
            self.missionaries_left < 0
            or self.cannibals_left < 0
            or self.missionaries_left > self.nof_missionaries
            or self.cannibals_left > self.nof_cannibals
        ):
            return False
        # number of cannibals can't exceed number of missionaries in either side
        if (
            self.cannibals_left > self.missionaries_left
            or self.cannibals_right > self.missionaries_right
        ):
            return False

        return True

    def get_next(self):
        """Returns the possible next states from the given state
        Args:
            state: type(State), current state to take an action
            action: type(str), action taken from the current state can be "left", "right"
        Returns:
            next states, type([State]), List of next possible reachable states

        Notes on possible actions:
        (Applicable to both side transitions)
        1C, 2C, 3C, 4C, 5C send
        -----------------------
        (1C, 1M), (2C, 2M) send
        -----------------------
        1M, 2M, 3M, 4M, 5M send

        """
        possible_states = []
        action = "right" if self.current_action == "left" else "left"
        if action == "left":
            for nof_passangers in range(1, self.boat_size + 1):
                # 1C, 2C, 3C, 4C, 5C send
                new_state = State(
                    self.missionaries_left,
                    self.cannibals_left - nof_passangers,
                    action
                )
                if new_state.is_reachable():
                    possible_states.append(new_state)

                # 1M, 2M, 3M, 4M, 5M send
                new_state = State(
                    self.missionaries_left - nof_passangers,
                    self.cannibals_left,
                    action
                )
                if new_state.is_reachable():
                    possible_states.append(new_state)

            for nof_passangers in range(1, 3):
                # (1C, 1M), (2C, 2M) send
                new_state = State(
                    self.missionaries_left - nof_passangers,
                    self.cannibals_left - nof_passangers,
                    action
                )
                if new_state.is_reachable():
                    possible_states.append(new_state)

        else:
            for nof_passangers in range(1, self.boat_size + 1):
                # 1C, 2C, 3C, 4C, 5C return
                new_state = State(
                    self.missionaries_left,
                    self.cannibals_left + nof_passangers,
                    action
                )
                if new_state.is_reachable():
                    possible_states.append(new_state)

                # 1M, 2M, 3M, 4M, 5M return
                new_state = State(
                    self.missionaries_left + nof_passangers,
                    self.cannibals_left,
                    action
                )
                if new_state.is_reachable():
                    possible_states.append(new_state)

            for nof_passangers in range(1, 3):
                # (1C, 1M), (2C, 2M) return
                new_state = State(
                    self.missionaries_left + nof_passangers,
                    self.cannibals_left + nof_passangers,
                    action
                )
                if new_state.is_reachable():
                    possible_states.append(new_state)
        return possible_states

    def __repr__(self):
        return "State()"

    def __str__(self):
        state_str = "{0:6s} {1:6s} {2:6s}".format(
            "C" * self.cannibals_left, "  " * 9, "C" * self.cannibals_right
        )
        state_str += "\n"
        state_str += "{0:6s} {1:6s} {2:6s}".format(
            "M" * self.missionaries_left, "  " * 9, "M" * self.missionaries_right
        )
        return state_str

    def __eq__(self, other):
        return (
            self.missionaries_left == other.missionaries_left
            and self.cannibals_left == other.cannibals_left
            and self.missionaries_right == other.missionaries_right
            and self.cannibals_right == other.cannibals_right
            and self.current_action == other.current_action
        )

    def __hash__(self):
        return hash(
            (
                self.missionaries_left,
                self.cannibals_left,
                self.missionaries_right,
                self.cannibals_right,
                self.current_action
            )
        )


def get_state_change_log(current_state, next_state):
    """Returns the string representation of state transition"""
    action = (
        "SEND"
        if (
            current_state.missionaries_left < next_state.missionaries_left
            or current_state.cannibals_left < next_state.cannibals_left
        )
        else "RETURN"
    )
    if action == "SEND":
        change_missionaries = abs(
            current_state.missionaries_left - next_state.missionaries_left
        )
        change_cannibals = abs(current_state.cannibals_left - next_state.cannibals_left)
    else:
        change_missionaries = abs(
            current_state.missionaries_right - next_state.missionaries_right
        )
        change_cannibals = abs(
            current_state.cannibals_right - next_state.cannibals_right
        )
    state_change = "{0:6s} {1:6s} {2:6s}".format(
        action,
        " " + str(change_cannibals) + " CANNIBALS",
        str(change_missionaries) + " MISSIONARIES",
    )

    return state_change


def nondeterministic_search(initial_state):
    """Performs nondeterministic to find possible solutions to the problem
    Args:
        intitial_state: type(State), initial state
    Returns:
        path: type([State]) list of states that visited throughout the search routine
    """
    if initial_state.is_goal():
        return [initial_state]

    # use to switch between both rowing actions
    # action_dict = {0: "left", 1: "right"}
    # action_flag = 1
    # being used to avoid loops
    current_path = [initial_state]
    queue = deque([current_path])
    while queue:
        visited = set()
        current_path = queue.popleft()
        current_state = current_path[len(current_path)-1]
        for state in current_path:
            visited.add(state)
        # action_flag = not action_flag
        if current_state.is_goal():
            return current_path
        next_states = current_state.get_next()
        for next_state in next_states:
            if next_state in visited:
                continue
            current_path.append(next_state)
            random_idx = randint(0, len(queue))
            if random_idx < len(queue):
                queue.insert(random_idx, current_path.copy())
            else:
                queue.append(current_path.copy())
            current_path.remove(next_state)


def print_solution(path):
    """Prints the solution from the given
    Args:
        path: type([State]) List of states obtained via nondeterministic search
    """
    prev = path[0]
    path_len = len(path)
    for i in range(1, path_len):
        print(prev)
        current = path[i]
        print(get_state_change_log(current, prev))
        prev = current
    print(prev)
    print('Solution consists of ' + str(path_len - 1) + ' river crossings' )


def main():
    """
    TODO(zcankara): Explain the problem
    TODO(zcankara): Add stepping argument
    """
    CANNIBALS = 6
    MISSIONARIES = 6
    initial_state = State(MISSIONARIES, CANNIBALS, "right")
    path = nondeterministic_search(initial_state)
    print_solution(path)


if __name__ == "__main__":
    main()
