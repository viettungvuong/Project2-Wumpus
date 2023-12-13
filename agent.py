from enum import Enum

from main import map
from kb import KB


class Direction(Enum):
    FORWARD = 1
    BACKWARD = 2
    LEFT = 3
    RIGHT = 4
    
# below function return a room that is in the given direction from the current room
def room_direction(current_room, direction):
    if direction == Direction.FORWARD:
        if current_room.y >= 0:
            return map[current_room.x][current_room.y - 1]
        else:
            return None
    elif direction == Direction.BACKWARD:
        if current_room.y <= 9:
            return map[current_room.x][current_room.y + 1]
        else:
            return None
    elif direction == Direction.LEFT:
        if current_room.x >= 0:
            return map[current_room.x - 1][current_room.y]
        else:
            return None
    elif direction == Direction.RIGHT:
        if current_room.x <= 9:
            return map[current_room.x + 1][current_room.y + 1]
        else:
            return None

class Agent:
    def __init__(self, current_room):
        self.current_room = current_room
        self.direction = Direction.RIGHT
        self.kb = KB()
        self.kb.add_sentence(f"A{current_room.x},{current_room.y}")
        self.kb.add_sentence(f"~W{current_room.x},{current_room.y}")
        self.kb.add_sentence(f"~P{current_room.x},{current_room.y}")

        self.visited_rooms = set()
        self.unvisited_safe_rooms = set()

    def moves(self):
        return list(Direction)

    def move(self, direction):
        next_room = room_direction(self.current_room, direction)
        if next_room is not None:
            self.current_room = next_room
        else:
            return

        if self.current_room.pit or self.current_room.wumpus:
            print("You died!")
            return
        elif self.current_room.gold:
            print("You collected gold!")

        self.percept()
        self.visited_rooms.add(self.current_room)

    def shoot(self):
        next_room = room_direction(self.current_room, self.direction)

        if next_room is not None:
            x = next_room.x
            y = next_room.y
            if map[x][y].wumpus:
                print("Wumpus screamed!")
                map[x][y].wumpus = False
                self.kb.add_sentence(f"~W{x},{y}")
                self.kb.add_sentence(f"~S{r[0]},{r[1]}" for r in map[x][y].surrounding_rooms)
            else:
                print("You missed!")

    def percept(self):
        if self.current_room.breeze: # if breeze
            self.kb.add_sentence(f"B{self.current_room.x},{self.current_room.y}")
            disjunction_sentences = []
            disjunction_sentences.append(f"P{r[0]},{r[1]}" for r in self.current_room.surrounding_rooms)
            self.kb.add_sentence(disjunction_sentences)
        else: # if not breeze
            self.kb.add_sentence(f"~B{self.current_room.x},{self.current_room.y}")
            self.kb.add_sentence(f"~P{r[0]},{r[1]}" for r in self.current_room.surrounding_rooms)

        if self.current_room.stench: # if stench
            self.kb.add_sentence(f"S{self.current_room.x},{self.current_room.y}")
            disjunction_sentences = []
            disjunction_sentences.append(f"W{r[0]},{r[1]}" for r in self.current_room.surrounding_rooms)
            self.kb.add_sentence(disjunction_sentences)
        else: # if not stench
            self.kb.add_sentence(f"~S{self.current_room.x},{self.current_room.y}")
            self.kb.add_sentence(f"~W{r[0]},{r[1]}" for r in self.current_room.surrounding_rooms)

    def safe_surrounding(self):
        for r in self.current_room.surrounding_rooms:
            if self.kb.check(f"W({r[0]},{r[1]})") and self.kb.check(f"P({r[0]},{r[1]})"):
                if map[r[0]][r[1]] not in self.visited_rooms:
                   self.unvisited_safe_rooms.add(map[r[0]][r[1]])
