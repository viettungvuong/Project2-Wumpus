from sympy import symbols, Function, satisfiable
from sympy.logic.boolalg import And, Implies, Not, BooleanFunction

current_agent_x = 0
current_agent_y = 0

Wumpus, Breeze, Pit, Stench, Gold, Okay = symbols('Wumpus Breeze Pit Stench Gold Okay', cls=Function)

# symbol
Dead = symbols('Dead', boolean=True)

okayLogic = Implies(And(Not(Pit(current_agent_x, current_agent_y)), Not(Wumpus(current_agent_x, current_agent_y))), Okay(current_agent_x, current_agent_y))

print(satisfiable(okayLogic))