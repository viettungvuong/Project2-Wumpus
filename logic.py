from pyDatalog import pyDatalog

pyDatalog.create_terms(
    "agent",
    "wumpus",
    "breeze",
    "gold",
    "pit",
    "stench",
    "dead",
    "okay"
)

okay(X,Y) <= ~pit(X,Y) & ~wumpus(X,Y) # room is okay
wumpus(X,Y) <= stench(X,Y) # wumpus is in room
pit(X,Y) <= breeze(X,Y) # pit is in room

dead <= ~okay(X,Y) & agent(X,Y) # agent is dead