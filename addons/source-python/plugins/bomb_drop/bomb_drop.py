import random
from core import GAME_NAME
from filters.players import PlayerIter
from entities.entity import Entity
from players.entity import Player
from commands.client import ClientCommand
from commands.server import ServerCommand
from messages import SayText2
from colors import GREEN, LIGHT_GREEN, RED

def load():
	if not GAME_NAME in ['cstrike', 'csgo']:
		raise ValueError(f'This plugin does not support {GAME_NAME.title()}')

choices = []

@ServerCommand('changelevel')
def map_change_command(args):
	''' Called when the map is about to be changed '''
	# Deletes players from random bomb giving target 
	del choices[:]

@ClientCommand('drop')
def drop_command(command, index):
	''' Called when player uses drop command '''
	# Define player at start to be use further use
	player = None
	# Checks is player valid
	try:
		# Create player object
		player = Player(index)
	# The player is not valid
	except ValueError:
		# Set player as invalid
		player = None
	# Well is the player valid
	if player:
		# Checks player current weapon
		try:
			# Get the current weapon that player is carrying
			weapon = player.get_active_weapon()
		# The weapon is invalid
		except AttributeError:
			# Set weapon to be invalid
			weapon = None
		# Well is the weapon valid and is it the bomb
		if weapon and weapon.classname == 'weapon_c4':
			try:
				# Tries find the world bomb
				entity = Entity.find('weapon_c4')
			# The world bomb was not found
			except AttributeError:
				# Set the bomb was not found
				entity = None
			# Well was it found
			if entity:
				try:
					# Check is there currently a delay running for bomb location checker
					running = bomb_delay.running
				# Checks is the delay valid
				except (ValueError, AttributeError, UnboundLocalError):
					# There is not currently running delay
					running = False
				# Well is it running
				if running:
					# It was running, now cancel it
					bomb_delay.cancel()
				# The delay was not running
				else:
					# Set delay for finding bomb location
					bomb_delay = entity.delay(20, find_location, (entity,))


def find_location(entity):
	# Is the bomb on the floor
	if entity.owner_handle in [-1, 0]:
		# Loop all players who are terrorist and alive
		for player in PlayerIter(['t', 'alive']):
			# Add players to list for chance to be selected for bomb giving
			choices.append(player)
		# Is there any players to be select
		if len(choices):
			# Get the random player who gets the bomb
			chosen = random.choice(choices)
			# Move the bomb location to the player
			entity.origin = chosen.origin
			# Tells in chat who got the bomb
			SayText2(f'{GREEN}[Bomb Checker] » {LIGHT_GREEN}The {GREEN}lost bomb {LIGHT_GREEN}was given {GREEN}randomly {LIGHT_GREEN}to {RED}{chosen.name}').send()
		# Deletes players from random bomb giving target 
		del choices[:]