

import core
import pyglet
from pyglet.window import key
from core import GameElement
from random import randint
import sys
import time

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
PLAYER2 = None
BORIS = None
######################

GAME_WIDTH = 7
GAME_HEIGHT = 7


# INitialize level 2
def initalize_level_two():

# Key positions
    block_positions = [
        (1,1),
        (5,5)
        ]

    blocks = []

    for pos in block_positions:
        block = Key()
        GAME_BOARD.register(block)
        GAME_BOARD.set_el(pos[0], pos[1], block)
        blocks.append(block)

    for block in blocks:
        print block

# Open Door position

    door = Door()
    GAME_BOARD.register(door)
    GAME_BOARD.set_el(3, 3,door)

    #reset players at corners
    GAME_BOARD.set_el(6,0,PLAYER)
    GAME_BOARD.set_el(0,6,PLAYER2)

    GAME_BOARD.draw_msg("Congrats!! Welcome to Level 2!")

def is_in_bounds(x,y):
    #check if dx or dy will put the key out of bounds
    if x < 0 or x > GAME_WIDTH - 1:
        return False
    # check if it went too far down or up, keep where it is if so
    if y < 0 or y > GAME_HEIGHT - 1:
        return False
    return True

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Treasure(GameElement):
    IMAGE = "Chest"
    SOLID = True    

    def interact(self, player):
        if len(player.inventory_gems) >= 5:
            if len(player.inventory_hearts) >= 1:
                GAME_BOARD.draw_msg("YOU ARE A WINNERRRR!!!!")
                GAME_BOARD.clear_board()
                player.inventory_gems = []
                global BORIS
                BORIS.update = do_nothing

                initalize_level_two()

                
            else:
                GAME_BOARD.draw_msg("MORE HEARTS!!")
        else:
            GAME_BOARD.draw_msg("YOU CANT OPEN THE TREASURE CHEST! MOAR GEMZ PLEEZ!")

    def cover_board(self):
        for x in range(0,GAME_WIDTH):
            for y in range(0,GAME_HEIGHT):
                existing_el = GAME_BOARD.get_el(x, y)
                if not existing_el or not existing_el.SOLID:
                    heart = Heart()
                    GAME_BOARD.register(heart)
                    GAME_BOARD.set_el(x, y, heart)

class Key(GameElement):
    IMAGE = "Key"
    SOLID = True 

    def interact(self, player):
        dx = self.x - player.x
        dy = self.y - player.y

        #check if dx or dy will put the key out of bounds
        if is_in_bounds(self.x + dx, self.y + dy):
            #move the key by dx and dy
            GAME_BOARD.del_el(self.x, self.y)
            GAME_BOARD.set_el(self.x + dx, self.y + dy, self)
            #move the player by dx and dy
            GAME_BOARD.del_el(player.x, player.y)
            GAME_BOARD.set_el(player.x + dx, player.y + dy, player)
    

class Door(GameElement):
    IMAGE = "DoorClosed"
    SOLID = True

    def openSesame(self):
        self.IMAGE = "DoorOpen"
        SOLID = True

class Character(GameElement):
    IMAGE = "Cat"
    SOLID = True

    def next_pos(self, direction):
        next_x = self.x
        next_y = self.y
        if direction == "up":
            next_y -= 1
        elif direction == "down":
            next_y += 1
        elif direction == "left":
            next_x -= 1
        elif direction == "right":
            next_x += 1

        # check if it went too far left or right, keep where it is if so
        if next_x < 0 or next_x > GAME_WIDTH - 1:
            next_x = self.x 
        # check if it went too far down or up, keep where it is if so
        if next_y < 0 or next_y > GAME_HEIGHT - 1:
            next_y = self.y

        return (next_x,next_y)
        # if direction == "up":
        #   return (self.x, self.y - 1)
        # elif direction ==  "down":
        #   return (self.x, self.y + 1)
        # elif direction == "left":
        #   return (self.x - 1, self.y)
        # elif direction == "right":
        #   return (self.x + 1, self.y)
        # return None

    def tell_inventory(self, message):
        GAME_BOARD.draw_msg("%s You have %d items! %d gems and %d hearts." % 
            (message, (len(self.inventory_gems) + len(self.inventory_hearts)),len(self.inventory_gems), len(self.inventory_hearts))) 


    def __init__(self):
        GameElement.__init__(self)
        self.inventory_gems = []
        self.inventory_hearts = []

class Friend(Character):
    IMAGE = "Princess"

    def __init__(self):
        Character.__init__(self)

def do_nothing(self):
    pass

class Enemy(Character):
    IMAGE = "Boy"

    def __init__(self):
        Character.__init__(self)

    def interact(self, player):
        self.inventory_gems = player. inventory_gems
        player.inventory_gems = []
        player.tell_inventory("The evil boy took all your gems!")
        
        # Taking Boris' gems and put them in the top row.
        gem_position = 0

        # we know this will break if there are lots of things in the top row. 
        while self.inventory_gems != []:
            gem = self.inventory_gems.pop()
            if GAME_BOARD.get_el(gem_position, 0) == None:
                GAME_BOARD.set_el(gem_position,0,gem)
            else:
                self.inventory_gems.append(gem)

            gem_position += 1

    
    def update(self, dt):
        if int(time.time() * 10) % 10== 0:
            boris_dir = randint(0,4)
            boris_next = None
            if boris_dir == 0:
                print "moving up"
                boris_next = BORIS.next_pos("up")
            elif boris_dir == 1:
                print "moving down"
                boris_next = BORIS.next_pos("down")
            elif boris_dir == 2:
                print "moving left"
                boris_next = BORIS.next_pos("left")
            else:
                print "moving right"
                boris_next = BORIS.next_pos("right")

            #move BORIS to his next position
            existing_el = GAME_BOARD.get_el(boris_next[0],boris_next[1])
            if existing_el is None:
                GAME_BOARD.del_el(BORIS.x, BORIS.y)
                GAME_BOARD.set_el(boris_next[0], boris_next[1], BORIS)

class Instructor(Character):
    IMAGE = "Girl"
    Solid = True

    def interact(self, player):

        Instructor_Number = randint(0, 2)
        print "random number is",Instructor_Number

        if Instructor_Number == 0 and len(player.inventory_gems) >= 1:
            player.inventory_gems.pop()
            player.tell_inventory("I AM LIZ! YOUR GEM IS MINE!!")
        elif Instructor_Number == 1:
            player.inventory_gems.append(Gem())
            player.tell_inventory("I AM LIZ! A GEM FOR YOU!!")
        else:
            player.tell_inventory("I AM LIZ! THANKS FOR SAYING HI!!")

class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False

    def interact(self, player):
        player.inventory_gems.append(self)
        player.tell_inventory("You just acquired a gem!")
        #GAME_BOARD.draw_msg("You just acquired a gem! You have %d items! %d gems and %d hearts." % ((len(player.inventory_gems) + len(player.inventory_hearts)),len(player.inventory_gems), len(player.inventory_hearts))) 

class Rupie(GameElement):
    IMAGE = "OrangeGem"
    SOLID = False

    def interact(self, player):
        # if direction:
        # next_location = PLAYER.next_pos(direction)
        # next_x = next_location[0]
        # next_y = next_location[1]

        GAME_BOARD.del_el(player.x, player.y)
        GAME_BOARD.set_el(0, 0, player)
        print "should have just reset player to 0,0"

class Heart(GameElement):
    IMAGE = "Heart"
    SOLID = False

    def interact(self, player):
        player.inventory_hearts.append(self)
        player.tell_inventory("You just got a heart!")

####   End class definitions    ####

def keyboard_handler():
    direction = None
    curr_player = None

    if KEYBOARD[key.UP]:
        direction = "up"
        curr_player = PLAYER
    elif KEYBOARD[key.DOWN]:
        direction = "down"
        curr_player = PLAYER
    elif KEYBOARD[key.RIGHT]:
        direction = "right"
        curr_player = PLAYER
    elif KEYBOARD[key.LEFT]:
        direction = "left"
        curr_player = PLAYER
    elif KEYBOARD[key.I]:
        direction = "up"
        curr_player = PLAYER2
    elif KEYBOARD[key.K]:
        direction = "down"
        curr_player = PLAYER2
    elif KEYBOARD[key.L]:
        direction = "right"
        curr_player = PLAYER2
    elif KEYBOARD[key.J]:
        direction = "left"
        curr_player = PLAYER2
    elif KEYBOARD[key.SPACE]:
        GAME_BOARD.erase_msg()

    if direction:
        next_location = curr_player.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]
        existing_el = GAME_BOARD.get_el(next_x, next_y)
        if existing_el is None or not existing_el.SOLID:
            #If there's nothing there or if the existing element is not solid, wlak through
            GAME_BOARD.del_el(curr_player.x, curr_player.y)
            GAME_BOARD.set_el(next_x, next_y, curr_player)
        if existing_el:
            existing_el.interact(curr_player)   


    # if int(time.time() * 10) % 10== 0:
    #     boris_dir = randint(0,4)
    #     boris_next = None
    #     if boris_dir == 0:
    #         print "moving up"
    #         boris_next = BORIS.next_pos("up")
    #     elif boris_dir == 1:
    #         print "moving down"
    #         boris_next = BORIS.next_pos("down")
    #     elif boris_dir == 2:
    #         print "moving left"
    #         boris_next = BORIS.next_pos("left")
    #     else:
    #         print "moving right"
    #         boris_next = BORIS.next_pos("right")

    #     #move BORIS to his next position
    #     existing_el = GAME_BOARD.get_el(boris_next[0],boris_next[1])
    #     if existing_el is None:
    #         GAME_BOARD.del_el(BORIS.x, BORIS.y)
    #         GAME_BOARD.set_el(boris_next[0], boris_next[1], BORIS)



def initialize():
    """Put game initialization code here"""

    # rock_positions = [
    #     (2, 1),
    #     (1, 2),
    #     (2, 3)
    #     # (1, 3),
    #     # (2, 2),
    #     # (3, 1),
    #     # (1, 1),
    #     # (3, 3)

    # ]

    # rocks = []

    # for pos in rock_positions:
    #     rock = Rock()
    #     GAME_BOARD.register(rock)
    #     GAME_BOARD.set_el(pos[0],pos[1],rock)
    #     rocks.append(rock)

    # for rock in rocks:
    #     print rock

    # rocks[-1].SOLID = False

    #initialize gems
    gem_positions = [
        (2, 3),
        (2, 2),
        (2, 4),
        (4, 2),
        (4, 3),
        (4, 4)
    ]
    gems = []

    for i in gem_positions:
        gem = Gem()
        GAME_BOARD.register(gem)
        GAME_BOARD.set_el(i[0],i[1],gem)
        gems.append(gem)


    chest = Treasure()
    GAME_BOARD.register(chest)
    GAME_BOARD.set_el(0,2,chest)

    Liz = Instructor()
    GAME_BOARD.register(Liz)
    GAME_BOARD.set_el(6, 3,Liz)

    #initialize Rupie
    rupie_positions = [
        (3, 2),
        (3, 4)

    ]

    rupies = []

    for pos in rupie_positions:
        rupie = Rupie()
        GAME_BOARD.register(rupie)
        GAME_BOARD.set_el(pos[0],pos[1],rupie)
        rupies.append(rupie)

    for rupie in rupies:
        print rupie


    #initalize hearts
    heart_positions = [
        (3,3),
        (6,6)
    ]

    hearts = []

    for pos in heart_positions:
        heart = Heart()
        GAME_BOARD.register(heart)
        GAME_BOARD.set_el(pos[0], pos[1], heart)
        hearts.append(heart)

    for heart in hearts:
        print heart


    # Initialize a girl character in the character class
    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(0, 6, PLAYER)
    print PLAYER

    global PLAYER2
    PLAYER2 = Friend()
    GAME_BOARD.register(PLAYER2)
    GAME_BOARD.set_el(6,0,PLAYER2)
    print PLAYER2

    global BORIS
    BORIS = Enemy()
    GAME_BOARD.register(BORIS)
    GAME_BOARD.set_el(3,6,BORIS)
    print BORIS

    GAME_BOARD.draw_msg("This game is hella awesome.")

