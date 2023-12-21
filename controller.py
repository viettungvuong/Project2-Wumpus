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
wn.bgcolor("black")
wn.title("A maze game")
wn.setup(600    ,600)

################################################################################
#Create pen
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=2, stretch_len=2)
        self.penup()
        self.speed(0)

################################################################################
#player
class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        # self.shape(gif_image_path_agent_right)
        self.shape("square")
        self.color("blue")
        self.shapesize(stretch_wid=2, stretch_len=2)
        self.penup()
        self.gold = 0
        self.speed(0)
    def go_up(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor()+48
        # self.shape(gif_image_path_agent_up)
        # print('##### \n')
        # print((move_to_x,move_to_y))
        # print('##### \n')
        # self.goto(move_to_x,move_to_y)
        if(move_to_x,move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)


    def go_down(self):
        # self.goto(self.xcor(), self.ycor() - 48)
        move_to_x = player.xcor()
        move_to_y = player.ycor() - 48
        # self.shape(gif_image_path_agent_down)

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)


    def go_left(self):
        # self.goto(self.xcor()-48, self.ycor())
        move_to_x = player.xcor() - 48
        move_to_y = player.ycor()
        # self.shape(gif_image_path_agent_left)

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)


    def go_right(self):
        # self.goto(self.xcor()+48, self.ycor())
        move_to_x = player.xcor() + 48
        move_to_y = player.ycor()
        # self.shape(gif_image_path_agent_right)

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

################################################################################
def setup_maze(map):
    for y in range(len(map)):
        for x in range(len(map[y])):
            #get the character at each x,y coordinate
            # Note the order of y and x in the next line
            character = map[x][y]
            screen_x = -250 + (x*48)
            screen_y = 250 - (y*48)

            #Check if it is an X
            if character == '-':
                pen.goto(screen_x,screen_y)
                pen.stamp()

            if character == 'A':
                player.goto(screen_x, screen_y)

################################################################################
#Create class instances
pen = Pen()
player = Player()

################################################################################
#Create walls,treasure
walls = []

################################################################################
#read file
map = read_file("map3.txt")
#setup the level
setup_maze(map)

# Keyboard controls
wn.listen()
wn.onkey(player.go_up, "Up")
wn.onkey(player.go_down, "Down")
wn.onkey(player.go_left, "Left")
wn.onkey(player.go_right, "Right")
# Main loop
wn.mainloop()