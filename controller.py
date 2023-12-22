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
#input game asset
import turtle
import math
from PIL import Image
#agent right
png_agent_right = "./asset/agent_right.png"
gif_agent_right = "./asset/agent_right.gif"
img = Image.open(png_agent_right)
img.save(gif_agent_right,"GIF")
turtle.register_shape(gif_agent_right)

#agent left
png_agent_left = "./asset/agent_left.png"
gif_agent_left = "./asset/agent_left.gif"
img = Image.open(png_agent_left)
img.save(gif_agent_left,"GIF")
turtle.register_shape(gif_agent_left)

#agent up
png_agent_up = "./asset/agent_up.png"
gif_agent_up = "./asset/agent_up.gif"
img = Image.open(png_agent_up)
img.save(gif_agent_up,"GIF")
turtle.register_shape(gif_agent_up)

#agent down
png_agent_down = "./asset/agent_down.png"
gif_agent_down = "./asset/agent_down.gif"
img = Image.open(png_agent_down)
img.save(gif_agent_down,"GIF")
turtle.register_shape(gif_agent_down)

#Pit
png_pit = "./asset/pit.png"
gif_pit = "./asset/pit.gif"
img = Image.open(png_pit)
img.save(gif_pit,"GIF")
# Resize the image
new_size = (40, 40)  # Set the new size (width, height)
resized_img = img.resize(new_size)
# Save the resized image as a GIF
resized_img.save(gif_pit, "GIF")
turtle.register_shape(gif_pit)

#Wumpus
png_wumpus = "./asset/wumpus.png"
gif_wumpus = "./asset/wumpus.gif"
img = Image.open(png_wumpus)
img.save(gif_wumpus,"GIF")
turtle.register_shape(gif_wumpus)

#Gold
png_gold = "./asset/gold.png"
gif_gold = "./asset/gold.gif"
img = Image.open(png_gold)
img.save(gif_gold,"GIF")
# Resize the image
new_size = (32, 32)  # Set the new size (width, height)
resized_img = img.resize(new_size)
# Save the resized image as a GIF
resized_img.save(gif_gold, "GIF")
turtle.register_shape(gif_gold)
################################################################################

wn = turtle.Screen()
wn.bgcolor("white")
wn.title("A maze game")
wn.setup(800,800)

#room
class Room():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pit = False
        self.wumpus = False
        self.stench = False
        self.breeze = False
        self.treasure = False

#pit
class Pit(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.hideturtle()
        self.shape(gif_pit)
        self.penup()
        self.speed(0)
#treasure
class Treasure(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.hideturtle()
        self.shape(gif_gold)
        self.penup()
        self.speed(0)
    def destroy(self):
        self.goto(2000,2000)
        self.hideturtle()

#player
class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        # self.shape(gif_image_path_agent_right)
        self.hideturtle()
        self.shape(gif_agent_right)
        # self.color("blue")
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
            self.shape(gif_agent_up)
    def is_collision(self,target):
        a = self.xcor() - target.xcor()
        b = self.ycor() - target.ycor()

        distance = math.sqrt((a**2) + (b**2))
        if distance < 20:
            return True
        else:
            return False


    def go_down(self):
        move_to_x = player.xcor()
        move_to_y = player.ycor() - 70

        # if (move_to_x, move_to_y) not in walls:
        if(move_to_y > -350):
            self.shape(gif_agent_down)
            self.goto(move_to_x, move_to_y)


    def go_left(self):
        move_to_x = player.xcor() - 70
        move_to_y = player.ycor()

        # if (move_to_x, move_to_y) not in walls:
        if(move_to_x > -350):
            self.shape(gif_agent_left)
            self.goto(move_to_x, move_to_y)


    def go_right(self):
        move_to_x = player.xcor() + 70
        move_to_y = player.ycor()
        # self.shape(gif_image_path_agent_right)

        # if (move_to_x, move_to_y) not in walls:
        if( move_to_x < 350):
            self.shape(gif_agent_right)
            self.goto(move_to_x, move_to_y)

################################################################################

def draw_maze(map):
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
                player.showturtle()

            if character == 'G':
                room_element.treasure = True
                gold = Treasure()
                gold.goto(screen_x+35,screen_y-50)
                treasures.append(gold)
                gold.showturtle()

            if character == 'P':
                pit = Pit()
                room_element.pit = True
                pit.goto(screen_x+35, screen_y-35)
                pits.append(pit)
                pit.showturtle()

            if character == 'W':
                room_element.wumpus = True

            room_line.append(room_element)
        rooms.append(room_line)

    ## add stench true and breeze true for each room

    for y in range(len(map)):
        for x in range(len(map[y])):
            if rooms[y][x].pit == True:
                # rooms[y][x].shape("square")
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
    while(True):
        for pit in pits:
            if player.is_collision(pit):
                print("Collision with pit")

        for treasure in treasures:
            if player.is_collision(treasure):
                print("Collision with gold")
        wn.update()

################################################################################
#read file
t = turtle.Turtle()
map = read_file("map1.txt")
player = Player()
pits = []
rooms = []
treasures = []

draw_maze(map)
turtle.done()

# print(rooms)
################################################################################

# Keyboard controls

# # Main loop
# wn.mainloop()