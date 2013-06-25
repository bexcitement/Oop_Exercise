import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 5
GAME_HEIGHT = 5

#### Put class definitions here ####
class Rock(GameElement):
	IMAGE = "Rock"
	SOLID = True

class Character(GameElement):
	IMAGE = "Cat"

	def next_pos(self, direction):
		if direction == "up":
			return (self.x, self.y - 1)
		elif direction ==  "down":
			return (self.x, self.y + 1)
		elif direction == "left":
			return (self.x - 1, self.y)
		elif direction == "right":
			return (self.x + 1, self.y)
		return None

	def __init__(self):
		GameElement.__init__(self)
		self.inventory = []

class Gem(GameElement):
	IMAGE = "BlueGem"
	SOLID = False

	def interact(self, player):
		player.inventory.append(self)
		GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!"%(len(player.inventory)))

class Rupie(GameElement):
	IMAGE = "OrangeGem"
	SOLID = False

	def interact(self, player):
		GAME_BOARD.del_el(player.x, player.y)
		GAME_BOARD.set_el(0, 0, player)
		print "should have just reset player to 0,0"

####   End class definitions    ####

def keyboard_handler():
	direction = None

	if KEYBOARD[key.UP]:
		GAME_BOARD.draw_msg("you pressed up")
		direction = "up"
		# next_y = PLAYER.y-1
		# GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
		# GAME_BOARD.set_el(PLAYER.x, next_y, PLAYER)
	elif KEYBOARD[key.DOWN]:
		GAME_BOARD.draw_msg("you pressed down!")
		direction = "down"
		# next_y = PLAYER.y+1
		# GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
		# GAME_BOARD.set_el(PLAYER.x, next_y, PLAYER)
	elif KEYBOARD[key.RIGHT]:
		GAME_BOARD.draw_msg("you pressed right!")
		direction = "right"
		# next_x = PLAYER.x+1
		# GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
		# GAME_BOARD.set_el(next_x, PLAYER.y, PLAYER)
	elif KEYBOARD[key.LEFT]:
		GAME_BOARD.draw_msg("you pressed left!")
		direction = "left"
		# next_x = PLAYER.x-1
		# GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
		# GAME_BOARD.set_el(next_x, PLAYER.y, PLAYER)
	elif KEYBOARD[key.SPACE]:
		GAME_BOARD.erase_msg()

	if direction:
		next_location = PLAYER.next_pos(direction)
		next_x = next_location[0]
		next_y = next_location[1]
		existing_el = GAME_BOARD.get_el(next_x, next_y)
		if existing_el:
			existing_el.interact(PLAYER)
		if existing_el is None or not existing_el.SOLID:
			#If there's nothing there or if the existing element is not solid, wlak through
			GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
			GAME_BOARD.set_el(next_x, next_y, PLAYER)			

def initialize():
    """Put game initialization code here"""
    # rock1 = Rock() # Creating rock1 
    # GAME_BOARD.register(rock1) # Registering rock1 on board
    # GAME_BOARD.set_el(1,1,rock1) # setting rock1 on board at this coordinate

    # # Initialize and register rock 2

    # rock2 = Rock()
    # GAME_BOARD.register(rock2)
    # GAME_BOARD.set_el(2, 2, rock2)

    # print "The first rock is at", (rock1.x,rock1.y) # print a string that states where the rock is based on x-y coordinates
    # print "The second rock is at", (rock2.x, rock2.y)
    # print "Rock 1 image", rock1.IMAGE
    # print "Rock 2 image", rock2.IMAGE

    rock_positions = [
    	(2, 1),
    	(1, 2),
    	(3, 2),
    	(2, 3)
    	# (1, 3),
    	# (2, 2),
    	# (3, 1),
    	# (1, 1),
    	# (3, 3)

    ]

    rocks = []

    for pos in rock_positions:
    	rock = Rock()
    	GAME_BOARD.register(rock)
    	GAME_BOARD.set_el(pos[0],pos[1],rock)
    	rocks.append(rock)

    for rock in rocks:
    	print rock

	rocks[-1].SOLID = False

	#initialize a gem
	gem = Gem()
	GAME_BOARD.register(gem)
	GAME_BOARD.set_el(3,1,gem)

	gem2 = Rupie()
	GAME_BOARD.register(gem2)
	GAME_BOARD.set_el(1,1,gem2)

	# Initialize a girl character in the character class
	global PLAYER
	PLAYER = Character()
	GAME_BOARD.register(PLAYER)
	GAME_BOARD.set_el(2, 2, PLAYER)
	print PLAYER

	GAME_BOARD.draw_msg("This game is hella awesome.")