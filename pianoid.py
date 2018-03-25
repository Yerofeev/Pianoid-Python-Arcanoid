import os
import sys

from menu import menu
import graphics

from resources import RESET_SETTINGS


def main():
	try:
		# check whether on POSIX-system
		import tty
		import termios
	except ImportError:
		print(
			'Unfortunately this OS is not currently supported!'
			'The game can be launched only in Linux.'
		)
		return
	rows, columns = os.popen('stty size', 'r').read().split()
	if int(rows) != 24 or int(columns) != 80:
		print(
			'Your terminal is ' + rows + 'x' + columns + '.'
			'The game can be launched only in 80x24-sized terminal.'
			' Open the standard-sized terminal and then start game again.'
		)
		return
	old_settings = termios.tcgetattr(sys.stdin)
	try:
		tty.setcbreak(sys.stdin.fileno())
		menu()
	finally:     # reset graphic settings on exit
		# reset graphic settings on exit
		print(RESET_SETTINGS)										   # reset colors
		os.system('setterm -cursor on')                                # return cursor
		os.system('clear')                                         	   # clear the screen
		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)  # restore terminal settings


if __name__ == '__main__':
	main()
