import random
from core import GAME_NAME
from filters.players import PlayerIter
from entities.entity import Entity
from players.entity import Player
from events import Event
from commands.client import ClientCommand
from commands.server import ServerCommand
from messages import SayText2
from colors import GREEN, LIGHT_GREEN, RED

def load():
	if not GAME_NAME in ['cstrike', 'csgo']:
		raise ValueError(f'This plugin does not support {GAME_NAME.title()}')

choices = []

@Event('player_hurt')
def player_hurt(args):
	# Checks is player valid
	try:
		# Create player object
		player = Player.from_userid(args['userid'])
		# Is the damage more than player health
		if args.get_int('dmg_health') >= player.health:
			# Loop every weapon player have
			for weapon in player.weapons():
				# Is the weapon bomb
				if weapon.classname == 'weapon_c4':
					# Start the bomb delay
					start_delay()
	except ValueError:
		# Player wasn't valid
		return

@ServerCommand('changelevel')
def map_change_command(args):
	''' Called when the map is about to be changed '''
	# Deletes players from random bomb giving target 
	del choices[:]

@ClientCommand('drop')
def drop_command(command, index):
	# Checks is player valid
	try:
		# Create player object
		player = Player(index)
		# Loop every weapon player have
		for weapon in player.weapons():
			# Is the weapon bomb
			if weapon.classname == 'weapon_c4':
				# Start the bomb delay
				start_delay()
	except ValueError:
		# Player wasn't valid
		return

def start_delay():
	# Find the bomb
	entity = Entity.find('weapon_c4')
	# Is there the bomb
	if entity:
		try:
			# Check is there currently a delay running
			running = bomb_delay.running
		# Checks is the delay valid
		except (AttributeError, UnboundLocalError):
			# The delay wasn't valid
			running = False
		# Delay is valid
		if running:
			# The delay is running cancel it
			bomb_delay.cancel()
			# Start new bomb delay
			bomb_delay = entity.delay(20, find_location, (entity,))
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
			# Select a random player who will receive the bomb
			chosen = random.choice(choices)
			# Move the bomb location to the player location
			entity.origin = chosen.origin
			# Tells in chat who got the bomb
			SayText2(f'{GREEN}[Bomb Checker] » {LIGHT_GREEN}The {GREEN}lost bomb {LIGHT_GREEN}was given {LIGHT_GREEN}to {RED}{chosen.name}').send()
		# Deletes players from random bomb giving target 
		del choices[:]
