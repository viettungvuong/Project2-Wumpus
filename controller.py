import agent
import time
room_height = 50
room_length = 50
half_room_height = room_height / 2
half_room_length = room_length / 2
offset_y = room_height * 5
offset_x = room_length * 5


def read_file(filename):
    # Read the content of the file
    with open(filename, "r") as file:
        content = file.readlines()

    # Extract size and map data
    size = int(content[0].strip())  # Extract size from the first line
    map_data = "".join(content[1:])

    # Process map data
    # print(map_data)
    map_rows = map_data.strip().split("\n")
    # print(map_rows)

    merged_rows = []
    for row in map_rows:
        merged_row = row.strip().split(".")
        merged_rows.append(merged_row)

    return merged_rows


# print(read_file("map2.txt"))
################################################################################
################################################################################
################################################################################
################################################################################
# input game asset
import turtle
import math
from PIL import Image

# agent right
png_agent_right = "./asset/agent_right.png"
gif_agent_right = "./asset/agent_right.gif"
img = Image.open(png_agent_right)
img.save(gif_agent_right, "GIF")
turtle.register_shape(gif_agent_right)

# agent left
png_agent_left = "./asset/agent_left.png"
gif_agent_left = "./asset/agent_left.gif"
img = Image.open(png_agent_left)
img.save(gif_agent_left, "GIF")
turtle.register_shape(gif_agent_left)

# agent up
png_agent_up = "./asset/agent_up.png"
gif_agent_up = "./asset/agent_up.gif"
img = Image.open(png_agent_up)
img.save(gif_agent_up, "GIF")
turtle.register_shape(gif_agent_up)

# agent down
png_agent_down = "./asset/agent_down.png"
gif_agent_down = "./asset/agent_down.gif"
img = Image.open(png_agent_down)
img.save(gif_agent_down, "GIF")
turtle.register_shape(gif_agent_down)

# Pit
png_pit = "./asset/pit.png"
gif_pit = "./asset/pit.gif"
img = Image.open(png_pit)
img.save(gif_pit, "GIF")
# Resize the image
new_size = (40, 40)  # Set the new size (width, height)
resized_img = img.resize(new_size)
# Save the resized image as a GIF
resized_img.save(gif_pit, "GIF")
turtle.register_shape(gif_pit)

# Wumpus
png_wumpus = "./asset/wumpus.png"
gif_wumpus = "./asset/wumpus.gif"
img = Image.open(png_wumpus)
img.save(gif_wumpus, "GIF")
turtle.register_shape(gif_wumpus)

# Gold
png_gold = "./asset/gold.png"
gif_gold = "./asset/gold.gif"
img = Image.open(png_gold)
img.save(gif_gold, "GIF")
# Resize the image
new_size = (32, 32)  # Set the new size (width, height)
resized_img = img.resize(new_size)
# Save the resized image as a GIF
resized_img.save(gif_gold, "GIF")
turtle.register_shape(gif_gold)

# Breeze
png_breeze = "./asset/breeze.png"
gif_breeze = "./asset/breeze.gif"
img = Image.open(png_breeze)
img.save(gif_breeze, "GIF")  # Resize the image
new_size = (32, 32)  # Set the new size (width, height)
resized_img = img.resize(new_size)
# Save the resized image as a GIF
resized_img.save(gif_breeze, "GIF")
turtle.register_shape(gif_breeze)

# Stench
png_stench = "./asset/stench.png"
gif_stench = "./asset/stench.gif"
img = Image.open(png_stench)
img.save(gif_stench, "GIF")
# Resize the image
new_size = (32, 32)  # Set the new size (width, height)
resized_img = img.resize(new_size)
# Save the resized image as a GIF
resized_img.save(gif_stench, "GIF")
turtle.register_shape(gif_stench)

# Unvisited
png_unvisited = "./asset/unvisited.jpg"
gif_unvisited = "./asset/unvisited.gif"
img = Image.open(png_unvisited)
img.save(gif_unvisited, "GIF")
# Resize
new_size = (room_height, room_length)  # Set the new size (width, height)
resized_img = img.resize(new_size)
# Save the resized image as a GIF
resized_img.save(gif_unvisited, "GIF")
turtle.register_shape(gif_unvisited)


# Frontier
png_frontier = "./asset/frontier.png"
gif_frontier = "./asset/frontier.gif"
img = Image.open(png_frontier)
img.save(gif_frontier, "GIF")
# Resize
new_size = (room_height, room_length)  # Set the new size (width, height)
resized_img = img.resize(new_size)
# Save the resized image as a GIF
resized_img.save(gif_frontier, "GIF")
turtle.register_shape(gif_frontier)

################################################################################
################################################################################
################################################################################
################################################################################

# room
class Room:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pit = False
        self.wumpus = False
        self.stench = 0
        # Truong hop dac biet la co 1 o trong giua 2 con wumpus
        # Khi con wumpus dau tien chet thi cai o ma between 2 con này vẫn co stench chu no ko bien mat
        self.breeze = False
        self.treasure = False


# pit
class Pit(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.hideturtle()
        self.shape(gif_pit)
        self.penup()
        self.speed(0)


# treasure
class Treasure(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.hideturtle()
        self.shape(gif_gold)
        self.penup()
        self.speed(0)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()


# breeze
class Breeze(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.hideturtle()
        self.shape(gif_breeze)
        self.penup()
        self.speed(0)


# stench
class Stench(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.hideturtle()
        self.shape(gif_stench)
        self.penup()
        self.speed(0)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()


# wumpus
class Wumpus(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.hideturtle()
        self.shape(gif_wumpus)
        self.penup()
        self.speed(0)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()


# unvisited
class Unvisited(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.hideturtle()
        self.shape(gif_unvisited)
        self.penup()
        self.speed(0)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()


# frontier
class Frontier(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.hideturtle()
        self.shape(gif_frontier)
        self.penup()
        self.speed(0)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()


# player
class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.hideturtle()
        self.shape(gif_agent_right)
        self.penup()
        self.gold = 0
        self.speed(0)

    def go_up(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() + room_height
        if move_to_y < room_height * 10:
            self.goto(move_to_x, move_to_y)
            self.shape(gif_agent_up)

    def is_collision(self, target):
        a = self.xcor() - target.xcor()
        b = self.ycor() - target.ycor()

        distance = math.sqrt((a**2) + (b**2))
        if distance < room_height/2:
            return True
        else:
            return False

    def go_down(self):
        move_to_x = player.xcor()
        move_to_y = player.ycor() - room_height

        if move_to_y > -room_height * 10:
            self.shape(gif_agent_down)
            self.goto(move_to_x, move_to_y)

    def go_left(self):
        move_to_x = player.xcor() - room_length
        move_to_y = player.ycor()

        if move_to_x > -room_length * 10:
            self.shape(gif_agent_left)
            self.goto(move_to_x, move_to_y)

    def go_right(self):
        move_to_x = player.xcor() + room_length
        move_to_y = player.ycor()

        if move_to_x < room_length * 10:
            self.shape(gif_agent_right)
            self.goto(move_to_x, move_to_y)
    
    def go_to(self,x,y):
        move_to_x = y
        move_to_y = -x
        self.shape(gif_agent_down)
        self.goto(move_to_x, move_to_y)
        


################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
# read file



def draw_map(map):
    offset = 0
    # Set line thickness and speed
    wn.tracer(0)
    t.pensize(4)
    # Draw vertical lines
    for i in range(len(map) + 1):
        t.penup()
        t.goto(
            offset - offset_x + i * room_length, offset_y
        )  # Start at top-left corner
        t.pendown()
        t.goto(
            offset - offset_x + i * room_length, offset_y - len(map) * room_height
        )  # Draw down to bottom

    # Draw horizontal lines
    for i in range(len(map) + 1):
        t.penup()
        t.goto(
            offset - offset_x, offset_y - i * room_height
        )  # Start at top-left corner
        t.pendown()
        t.goto(
            offset - offset_x + len(map[0]) * room_length, offset_y - i * room_height
        )  # Draw across to right

    # draw frontier and unvisited
    for room in frontier:
        screen_x = offset - offset_x + room.x * room_length + room_length / 2
        screen_y = offset_y - room.y * room_height - room_height / 2
        frontier_room = Frontier()
        frontier_room.goto(screen_x, screen_y)
        frontier_room.showturtle()
    for room in unvisited:
        screen_x = offset - offset_x + room.x * room_length + room_length / 2
        screen_y = offset_y - room.y * room_height - room_height / 2
        unvisited_room = Unvisited()
        unvisited_room.goto(screen_x, screen_y)
        unvisited_room.showturtle()

    # Set image for agent, gold, pit, wumpus
    for y in range(len(map)):
        room_line = []  # line 1,2,3,4 ....
        for x in range(len(map[y])):
            character = map[y][x]
            screen_x = offset - offset_x + x * room_length
            screen_y = offset_y - y * room_height
            room_element = Room(y, x)  # room[x] in line[y]

            if character == "A":
                player.goto(screen_x + half_room_length, screen_y - half_room_height)
                player.showturtle()

            if character == "G":
                room_element.treasure = True
                gold = Treasure()
                gold.goto(
                    screen_x + half_room_length,
                    screen_y - half_room_height + room_height / 4,
                )
                treasures.append(gold)
                gold.showturtle()

            if character == "P":
                pit = Pit()
                room_element.pit = True
                pit.goto(screen_x + half_room_length, screen_y - half_room_height)
                pits.append(pit)
                pit.showturtle()

            if character == "W":
                room_element.wumpus = True
                wumpus = Wumpus()
                wumpus.goto(screen_x + half_room_length, screen_y - half_room_height)
                wumpuses.append(wumpus)
                wumpus.showturtle()

            room_line.append(room_element)
        rooms.append(room_line)  # add line[y] to rooms (rooms is 2-d array)

    ## add stench true and breeze true for each room
    for y in range(len(map)):
        for x in range(len(map[y])):
            if rooms[y][x].pit == True:
                # rooms[y][x].shape("square")
                if x + 1 < len(map) and rooms[y][x + 1].pit == False:
                    rooms[y][x + 1].breeze = True
                if x - 1 >= 0 and rooms[y][x - 1].pit == False:
                    rooms[y][x - 1].breeze = True
                if y + 1 < len(map) and rooms[y + 1][x].pit == False:
                    rooms[y + 1][x].breeze = True
                if y - 1 >= 0 and rooms[y - 1][x].pit == False:
                    rooms[y - 1][x].breeze = True
            if rooms[y][x].wumpus == True:
                if x + 1 < len(map) and rooms[y][x + 1].pit == False:
                    rooms[y][x + 1].stench += 1
                if x - 1 >= 0 and rooms[y][x - 1].pit == False:
                    rooms[y][x - 1].stench += 1
                if y + 1 < len(map) and rooms[y + 1][x].pit == False:
                    rooms[y + 1][x].stench += 1
                if y - 1 >= 0 and rooms[y - 1][x].pit == False:
                    rooms[y - 1][x].stench += 1

    breeze_offset_x = room_length / 2
    breeze_offset_y = room_height / 2
    stench_offset_x = room_length / 2
    stench_offset_y = room_height / 2
    # draw breeze + stench
    for y in range(len(map)):
        for x in range(len(map[y])):
            screen_x = offset - offset_x + x * room_length
            screen_y = offset_y - y * room_height
            if rooms[y][x].breeze == True:
                # print("Room", (y, x), "::::", rooms[y][x].breeze)
                breeze = Breeze()
                breeze.goto(screen_x + breeze_offset_x, screen_y - breeze_offset_y)
                breezes.append(breeze)  # append to check collison
                breeze.showturtle()

            if rooms[y][x].stench > 0:
                stench = Stench()
                stench.goto(screen_x + stench_offset_x, screen_y - stench_offset_y)
                stenches.append(stench)  # append to check collison
                stench.showturtle()

    wn.update()
    
    for move in agent.moves:
        player.go_to(offset-offset_x+move[0].x * room_length + room_length/2,offset-offset_y+ move[0].y * room_height + room_height/2)
        if move[1] == 'None':
            pass
        elif move[1] == "Shot Wumpus":
            for wumpus in wumpuses:
                if player.is_collision(wumpus):
                    print("collision with wumpus")
                    wumpuses.remove(wumpus)
                    wumpus.destroy()
                    wn.update()
        elif move[1] == "Gold":
            for treasure in treasures:
                if player.is_collision(treasure):
                    print("collision with treasure")
                    treasures.remove(treasure)
                    treasure.destroy()
                    wn.update()
            pass
        
        wn.update()  
        time.sleep(0.5)

wn = turtle.Screen()
wn.bgcolor("white")
wn.title("A maze game")
wn.setup(1.0, 1.0)         
turtle.screensize(canvwidth=turtle.window_width(), canvheight=turtle.window_height())
t = turtle.Turtle()
map = read_file("map5.txt")

##create instances
player = Player()
pits = []
rooms = []
treasures = []
breezes = []
stenches = []
wumpuses = []

# thuat toan se luu state vao trong unvisted va frontier r draw ra
unvisited = []
frontier = []



# Draw the map
draw_map(map)
turtle.done()
