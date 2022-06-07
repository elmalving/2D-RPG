from playerStats import Player
from gameDisplay import gameDisplay
from itemList import *  # noqa, generates items to exist
player = Player()
menu = gameDisplay(player=player)
menu.showMenu()
