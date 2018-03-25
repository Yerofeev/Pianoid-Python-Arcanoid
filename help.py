# coding: utf-8
import os
from time import sleep


from graphics import help_paint, print_there
from engine import is_data, get_key
from resources import *


def page_1(x=1):
	os.system('clear')
	text = '''
	Pianoid is yet another arcanoid-game. Your paddle is a piano. The goal\n  is to clear the level by crashing the bricks with a ball. To assist you with\n  this arduous task you will encounter many types of prizes, listed on the next\n  page. 
	Besides the task to smash the bricks, you should evade monsters, there\n  are plenty of them on each level! After nine levels you will meet the Boss\n  Monster, where you will need all the skills acquired in the previous levels. 
   	There are several types of mosnters: Python-snake, clouds and zipper-\n  mouth foe. They start appearing after (4,6)seconds on common levels and after\n  (0,2)s on boss level and will occasionally drop bombs, so stay ready to dodge.\n  If bomb hits the piano, you will lose one live, but level won't be restarted\n  and balls are not stopped.
   	Monsters will attempt to destroy you with bombs, fire and to turn your\n  piano soundless. Some bricks will regenerate after a certain amount of time,\n  obfuscating your path towards the victory.Tips to cope with that are given at\n  the last page.The game goes on until there are lives left (by default there\n  are 4), when no balls left or Esc is pressed you lose one life. Already\n  destructed bricks on this floor are not respawned, if lives left more than 0.    	
	  '''
	print_there(x+33, 2, PIANO + BLANK*2 + BREND + BLANK + RESET_SETTINGS + PIANO + BLANK)
	print_there(x+33, 3, DASH * 13)
	print_there(x, 3, colors[3] + italic + text)
	help_paint()
	print_there(23, 23, colors[4] + bold + 'Press Esc to exit to menu')
	print_there(55, 23, colors[0] + '1/3 ')
	print_there(x+65, 23, colors[0] + bold + '⟿  ')


def page_2(x=5):
	y = 4
	os.system('clear')
	print_there(x+22, y-2, PRIZES_HELP)
	print_there(x, y, EXTEND + extend_font)
	print_there(x+20, y, colors[3] + italic + 'Extend the piano')
	print_there(x, y+1, SHRINK + shrink_font)
	print_there(x+20, y+1, colors[3] + italic + 'Shrink the piano')
	print_there(x, y+2, NEW_BALL + new_ball_font)
	print_there(x+20, y+2, colors[3] + italic + 'Extra ball')
	print_there(x, y+3, GLUE + glue_font)
	print_there(x+20, y+3, colors[3] + italic + 'Glue. Ball is stuck to piano every time it lands on it. \n' + BLANK*24 + "Press 'Space' to launch the ball again")
	print_there(x, y+5, FASTER + faster_font)
	print_there(x+20, y+5, colors[3] + italic + 'Speed up the ball')
	print_there(x, y+6, SLOWER + slower_font)
	print_there(x+20, y+6, colors[3] + italic + 'Slow down the ball')
	print_there(x, y+7, ''.join(BOMBS))
	print_there(x+20, y+7,  colors[3] + italic + 'If you catch  those ones you will lose one life')
	print_there(x, y + 8, EXTRA_LIFE + extra_life_font)
	print_there(x + 20, y + 8, colors[3] + italic + 'Extra life')
	print_there(x, y+9, PROTECTION[1] + protection_font)
	print_there(x + 20, y + 9, colors[3] + italic + 'Protects you from bombs and lightnings')
	print_there(x, y + 10, BARLINE + barline_font)
	print_there(x + 20, y + 10, colors[3] + italic + 'Lines appear at the bottom so the ball will not drop.\n' + BLANK*24 + 'Start blinking when about to dissipate')
	print_there(x, y+12, AUTOPILOT + autopilot_font)
	print_there(x + 20, y + 12, colors[3] + italic + 'Named after my favorite pianist. Autopilot for several\n' + BLANK*24 + 'seconds. Also blinking when effect will soon wear off')
	print_there(x, y+14, FIRE + fire_font)
	print_there(x + 20, y + 14, colors[3] + italic + 'Burst laser to crash adversaries, monsters and bricks!')
	print_there(x , y+15, '\b' + SURPRISE + surprise_font)
	print_there(x + 20, y + 15, colors[3] + italic + 'Random prize: Fire, Death - 2%\n' + BLANK*24 + 'Autopilot, Barlines, Extra Life, Glue - 6%\n' + BLANK*24 + 'The rest  - 12%')
	help_paint()
	print_there(23, 23, colors[4] + bold + 'Press Esc to exit to menu')
	print_there(55, 23, colors[0] + '2/3 ')
	print_there(x + 5, 23, colors[0] + bold + '⬳  ')
	print_there(x + 65, 23, colors[0] + bold + '⟿  ')


def page_3(x=2):
	os.system('clear')

	text = '''
    -Lifts: on some levels there are elevators that instantly relocate the ball.
    -When both fire and glue modes are active, you will simultaneously shoot\n  and launch the balls, because the same key is responsible for both actions.
    -There are several types of blinking bricks, that will regenerate after a\n  certain time. You don't have to destruct them in order to finish the level
    -If headphones color is dim, you are protected from one bomb or fire shot,\n  if bright - then from 2 or more
    -When the ball hits the monster - the latter will explode, the former's\n  direction will randomly change. So beware!
    -During autopilot the prizes are only occasionally caught.
    -Extension prize has its downsides: possibility of being hit by bombs is\n  increased and undesired prizes might be caught. So make your tradeoff!
    -Monsters on the boss levels are more prone to drop bombs near borders.
  
		  '''
	print_there(27, 2, TIPS)
	print_there(1, 4, colors[3] + italic + text)
	print_there(23, 23, colors[4] + bold + 'Press Esc to exit to menu')
	print_there(55, 23, colors[0] + '3/3 ')
	print_there(x + 5, 23, colors[0] + bold + '⬳  ')
	help_paint()


def info():
	k = 1
	page_1()
	page = [page_1, page_2, page_3]
	while True:
		if is_data():
			key_pressed = get_key()
			if key_pressed == 27:
				return
			elif key_pressed == 67 and k < 3:
				k += 1
				page[k-1]()
			elif key_pressed == 68 and k > 1:
				k -= 1
				page[k-1]()
