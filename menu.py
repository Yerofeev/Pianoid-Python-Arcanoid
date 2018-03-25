import termios
import threading
import sys
from time import sleep, time

from engine import is_data, get_key, game_proc
from graphics import print_there, preliminaries, menu_paint
from resources import *
import help


def moving_pointer(x, y, direction):
	print_there(x - 2, y, BLANK*2)
	print_there(x - 2, y + 2*direction, CLEF)
	return y + 2*direction


def levels_choice(x, y):
	y = moving_pointer(x, y, -1)
	for i in range(4):
		print_there(35, y + i * 2, BLANK * 12)
	print_there(35, y, RETURN_MENT)
	for i in range(2, 6):
		print_there(35, y+i*2-2, BLANK*3 + level_font_menu + BLANK + str(i*2-1))    # choose level [3,5,7,9]
	while True:
		if is_data():
			key_pressed = get_key()
			if key_pressed == 65 and y >= 12:     # up
				y = moving_pointer(x, y, -1)
			elif key_pressed == 66 and y <= 16:    # down
				y = moving_pointer(x, y, 1)
			elif key_pressed == 27 and y <= 14:    # Esc
				return 10
			elif key_pressed == 10:
				return y


def menu():
	while True:
		x = 35
		y = 10
		# flush stdin when returning from game_proc
		termios.tcflush(sys.stdin, termios.TCIOFLUSH)
		# and set default level == 1
		current_level = 1
		menu_paint(x, y)
		while True:
			if is_data():
				key_pressed = get_key()
				if key_pressed == 65 and y >= 12:
					y = moving_pointer(x, y, -1)
				elif key_pressed == 66 and y <= 14:
					y = moving_pointer(x, y, 1)
				elif key_pressed == 10:
					if y == 10:
						game_proc(current_level)
						break
					elif y == 12:
						y = levels_choice(x, y)
						current_level = y - 9
						if y == 10:
							break
						elif y > 0:
							sleep(0.5)
							game_proc(current_level)
							break
					elif y == 14:
						help.info()
						print_there(35, 14, BLANK * 2)
						y = 10
						break
					elif y == 16:
						return
				elif key_pressed == 27:
					return



if __name__ == '__main__':
		menu()
