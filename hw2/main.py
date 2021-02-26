import copy
import state
from state import State

initial_state = State()
a = initial_state.get_next()
for b in a:
    b.print()