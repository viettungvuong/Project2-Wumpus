def read_file(filename):
    # Read the content of the file
    with open(filename, "r") as file:
        content = file.readlines()

    # Extract size and map data
    size = int(content[0].strip())  # Extract size from the first line
    map_data = ''.join(content[1:])

    # Process map data
    # print(map_data)
    map_rows = map_data.strip().split('\n')
    # print(map_rows)

    merged_rows = []
    for row in map_rows:
        merged_row = row.strip().split('.')
        merged_rows.append(merged_row)

    return merged_rows

# print(read_file("map2.txt"))

################################################################################

import turtle
import math
wn = turtle.Screen()
wn.bgcolor("white")
wn.title("A maze game")
wn.setup(800,800)

#room
class Room():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.pit = False
        self.wumpus = False
        self.stench = False
        self.breeze = False
        self.treasure = False

#player
class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        # self.shape(gif_image_path_agent_right)
        self.shape("square")
        self.color("blue")
        self.shapesize(stretch_wid=2.56, stretch_len=2.56)
        self.penup()
        self.gold = 0
        self.speed(0)
    def go_up(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor()+70
        # if(move_to_x,move_to_y) not in walls:
        if(move_to_y < 350):
            self.goto(move_to_x, move_to_y)


    def go_down(self):
        move_to_x = player.xcor()
        move_to_y = player.ycor() - 70

        # if (move_to_x, move_to_y) not in walls:
        if(move_to_y > -350):
         self.goto(move_to_x, move_to_y)


    def go_left(self):
        move_to_x = player.xcor() - 70
        move_to_y = player.ycor()

        # if (move_to_x, move_to_y) not in walls:
        if(move_to_x > -350):
            self.goto(move_to_x, move_to_y)


    def go_right(self):
        move_to_x = player.xcor() + 70
        move_to_y = player.ycor()
        # self.shape(gif_image_path_agent_right)

        # if (move_to_x, move_to_y) not in walls:
        if( move_to_x < 350):
            self.goto(move_to_x, move_to_y)

################################################################################

def draw_maze(map):
    t = turtle.Turtle()
    # Set line thickness and speed
    t.pensize(4)
    t.speed(0)
    # print(len(map))
    # Draw vertical lines
    for i in range(len(map)+1):
        t.penup()
        t.goto(-350 + i * 70, 350)  # Start at top-left corner
        t.pendown()
        t.goto(-350 + i * 70, -350+(10-len(map))*70)  # Draw down to bottom

    # Draw horizontal lines
    for i in range(len(map)+1):
        t.penup()
        t.goto(-350, 350 - i * 70)  # Start at top-left corner
        t.pendown()
        t.goto(350 - (10-len(map))*70, 350 - i * 70)  # Draw across to right

    for y in range(len(map)):
        room_line = []
        for x in range(len(map[y])):
            character = map[y][x]
            screen_x = -350 + (x * 70)
            screen_y = 350 - (y * 70)
            room_element = Room(y,x)
            if character == 'A':
                player.goto(screen_x+35, screen_y-35)

            if character == 'G':
                room_element.treasure = True

            if character == 'P':
                room_element.pit = True
                # print(y,x)

            if character == 'W':
                room_element.wumpus = True

            room_line.append(room_element)
        rooms.append(room_line)

    ## add stench true and breeze true for each room

    for y in range(len(map)):
        for x in range(len(map[y])):
            if rooms[y][x].pit == True:
                if x+1 < len(map): rooms[y][x+1].breeze = True
                if x-1 >= 0: rooms[y][x-1].breeze = True
                if y+1 < len(map): rooms[y+1][x].breeze = True
                if y-1 >= 0: rooms[y-1][x].breeze = True
            if rooms[y][x].wumpus == True:
                if x+1 < len(map): rooms[y][x + 1].stench = True
                if x-1 >= 0: rooms[y][x - 1].stench = True
                if y+1 < len(map): rooms[y + 1][x].stench = True
                if y-1 >= 0: rooms[y - 1][x].stench = True
    #Test
    # for y in range(len(map)):
    #     for x in range(len(map[y])):
    #         print("Room: ", (y,x), " has: \n")
    #         print("PIT: ",rooms[y][x].pit)
    #         print("\n")
    #         print("Wumpus: ", rooms[y][x].wumpus)
    #         print("\n")
    #         print("Gold: ", rooms[y][x].treasure)
    #         print("\n")
    #         print("Breeze: ", rooms[y][x].breeze)
    #         print("\n")
    #         print("Stench: ", rooms[y][x].stench)
    #         print("\n")

    # print("Room: ", (9, 9), " has: \n")
    # print("PIT: ", rooms[1][1].pit)
    # print("\n")
    # print("Wumpus: ", rooms[1][1].wumpus)
    # print("\n")
    # print("Gold: ", rooms[1][1].treasure)
    # print("\n")
    # print("Breeze: ", rooms[1][1].breeze)
    # print("\n")
    # print("Stench: ", rooms[1][1].stench)
    # print("\n")

    wn.listen()
    wn.onkey(player.go_up, "Up")
    wn.onkey(player.go_down, "Down")
    wn.onkey(player.go_left, "Left")
    wn.onkey(player.go_right, "Right")
    turtle.done()

################################################################################
#read file
map = read_file("map1.txt")
player = Player()
rooms = []


draw_maze(map)

# print(rooms)
################################################################################

# Keyboard controls

# # Main loop
# wn.mainloop()