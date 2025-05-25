import random
from core import GAME_NAME
from listeners.tick import Repeat
from filters.players import PlayerIter
from entities.entity import Entity
from messages import SayText2
from messages.colors.saytext2 import GREEN, RED, BRIGHT_GREEN as LIGHT_GREEN

def load():
    if GAME_NAME != 'cstrike':
        raise ValueError('[Bomb Checker] This plugin only supports Counter-Strike: Source.')

BOMB_GIVEN = SayText2('{GREEN}[Bomb Checker] » {LIGHT_GREEN}The lost bomb has been given to {RED}{name}')

@Repeat
def find_dropped_bomb():
    bomb = Entity.find('weapon_c4')
    if bomb is None:
        return

    if bomb.owner_handle != 0:
        return

    t_alive_players = list(PlayerIter(['t', 'alive']))

    if not t_alive_players:
        return

    selected_player = random.choice(t_alive_players)
    bomb.origin = selected_player.origin
    BOMB_GIVEN.send(GREEN=GREEN, RED=RED, LIGHT_GREEN=LIGHT_GREEN, name=selected_player.name)
