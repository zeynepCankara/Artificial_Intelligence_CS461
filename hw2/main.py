import state
from state import State

initial_state = State()
initial_state.print()
new_state = initial_state.up()
initial_state.print()