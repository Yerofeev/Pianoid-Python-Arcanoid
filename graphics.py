import os
import sys
import random
from time import sleep
from resources import *


def print_there(x, y, text):
	"""Simply print text at the specific place(x,y) on the screen"""
	sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y, x, text))
	sys.stdout.flush()
	return


def preliminaries(current_level):
	"""CLear the screen, remove the cursor, draw the borders, prizes and monsters annotations"""
	os.system('clear')
	os.system('setterm -cursor off')
	print_there(0, 0, BASS_CLEF + MUSICAL_STAFF*61 + BASS_CLEF)
	for i in range(1, 23):
		print_there(0, i + 1, REPRISE_LEFT + BLANK*60 + REPRISE_RIGHT)
	x = 65
	y = 1
	if current_level not in boss_levels:
		for j in range(2, 23):
			for i in random.sample(range(2, 62), random.randint(0, 2)+1):
				print_there(i, j, random.choice(colors[:11]) + italic + random.choice(symbols))
	print_there(x+3, y,  monsters_font)
	print_there(x, y+1, BLANK*2 + MONSTER_1 + BLANK + MONSTER_2 + BLANK + HINDRANCE_2 + BLANK + HINDRANCE_1)
	print_there(x+1, y + 2, ''.join(BOMBS))
	print_there(x-1, y+3, DASH*17)
	print_there(x-1, y+4, SURPRISE + surprise_font)     # x-1 in order to align
	print_there(x, y+5, EXTEND + extend_font)
	print_there(x, y+6, SHRINK + shrink_font)
	print_there(x, y+7, NEW_BALL + new_ball_font)
	print_there(x, y+8, GLUE + glue_font)
	print_there(x, y+9, EXTRA_LIFE + extra_life_font)
	print_there(x, y+10, SLOWER + slower_font)
	print_there(x, y+11, FASTER + faster_font)
	print_there(x, y+12, PROTECTION[1] + protection_font)         # correct font
	print_there(x, y+13, BARLINE + barline_font)
	print_there(x, y+14, AUTOPILOT + autopilot_font)
	print_there(x, y+15, FIRE + fire_font)
	print_there(x-1, y+16, DASH*17)
	print_there(x, y+17, fire_instr)
	print_there(x, y+18, pause_font + BLANK + quit_font)
	print_there(x, y+19, exit_font)
	print_there(x+1, y+20, level_font + str(current_level))
	print_there(x-1, y+21, DASH*17)


def draw_moving_object(x, y, obj, pause, speed=0.1, b=4):
	"""Drawing falling prizes, moving balls, by default speed of falling prize, pause is necessary
	here to be able to stop the game when the object is displayed - see the code below.
	b- number of BLANKs,4 by default"""
	print_there(x, y, obj)
	sleep(speed)
	pause.wait()
	print_there(x, y, BLANK * b)


def paint_explosion(x, y, rate=0.03):
	"""Explosion"""
	print_there(x, y, EXPLOSION[1])
	sleep(rate)
	print_there(x, y, EXPLOSION[2])
	sleep(rate)
	print_there(x, y, BLANK)


# ------------------------------FIZZLE ALG------------------------------- #
def fizzle_gen():
	a = list(range(1920))
	for _ in range(1920):
		i = random.choice(a)
		a.remove(i)
		x = i % 80
		y = i // 80
		yield x, y


def fizzle(font, rate=0.0007):
	"""Fizzling algorithm, fills the screen with certain color or symbol"""
	for i in fizzle_gen():
		sleep(rate)
		print_there(i[0], i[1], font)


# -------------------------------LIFT -------------------------------------#
def draw_lift(lift):
	print_there(lift[0][0], lift[0][1], LIFT)
	print_there(lift[1][0], lift[1][1], LIFT)


# ------------------------------for Barline prizes -----------------------#
def paint_barlines():
	for i in range(30):
		print_there(32+i, 24, barline)
		print_there(32-i, 24, barline)
		sleep(0.005)


def borders_monster(y, mode=0):
	"""Erase and redraw two borders block to let monsters to sneak in"""
	if mode == 0:
		print_there(0, y, BLANK)
		print_there(63, y, BLANK)
	if mode == 1:
		print_there(0, y, REPRISE_LEFT)
		print_there(63, y, REPRISE_RIGHT)


def menu_paint(x, y):
	x0 = 0
	os.system('clear')
	os.system('setterm -cursor off')
	print_there(0, 0, BASS_CLEF + MUSICAL_STAFF*78 + BASS_CLEF)
	# ---------------------------------menu borders--------------------------------------------------------------#
	for i in range(1, 23):
		print_there(
					0, i + 1, REPRISE_LEFT + BLANK * 25 + REPRISE_RIGHT + BLANK * 23
					+ REPRISE_LEFT + BLANK * 25 + REPRISE_RIGHT)
		print_there(29, i+1, red_note + 22*BLANK + red_note)
		print_there(30, i + 1, yellow_note + 20 * BLANK + yellow_note)
		print_there(x + 1, y, NEW_GAME)
		print_there(x+3, y + 2, CHOOSE_LEVEL)
		print_there(x + 4, y + 4, HELP)
		print_there(x + 4, y + 6, QUIT)
		print_there(x - 2, y, CLEF)
	print_there(30, 2, 23*red_note)
	print_there(30, 3, 22 * yellow_note)
	print_there(30, 23, 23*red_note)
	print_there(30, 22, 22 * yellow_note)
	print_there(0, 24, 80*MUSICAL_STAFF)
	print_there(35, 6, PIANO + BLANK*2 + BREND + BLANK + RESET_SETTINGS + PIANO + BLANK)
	print_there(35, 7, DASH * 13)
	# ---------------------------------demo image----------------------------------------------------------------#
	print_there(x0+6, 23, PIANO * 8)
	print_there(x0+8, 20, BALL)
	print_there(x0+21, 9, BALL)
	print_there(x0+11, 5, BALL)
	print_there(x0+22, 7, EXTEND)
	print_there(x0+5, 10, SHRINK)
	print_there(x0+3, 5, SURPRISE)
	print_there(x0+13, 13, SLOWER)
	print_there(x0+23, 19, DEATH_1)
	for i in range(5):
			print_there(x0+i*5+2, 2, (lambda z: (b1[0]) if i % 2 == 0 else b2[0])(i))
	for i in range(5):
		print_there(x0 + i * 5 + 2, 3, (lambda z: (b3[0]) if i % 2 != 0 else (b2[0]))(i))
	for i in range(3):
		print_there(x0 + i * 5 + 12, 4, (lambda z: (b0[0]) if i % 2 == 0 else b4[0])(i))
	x0 += 52
	print_there(x0+16, 23, PIANO * 10)
	print_there(x0+21, 11, MONSTER_1)
	print_there(x0+6, 9, FASTER)
	print_there(x0+3, 5, BALL)
	print_there(x0+22, 7, EXTEND)
	print_there(x0+22, 14, BOMBS[1])
	print_there(x0+13, 12, EXTRA_LIFE)
	print_there(x0 + 5, 14, FIRE)
	print_there(x0+14, 19, BALL)
	for i in range(5):
			print_there(x0+i*5+2, 2, (lambda z: b8[0] if i % 2 == 0 else b1[0])(i))
	for i in range(5):
		print_there(x0 + i * 5 + 2, 3, (lambda z: b112[0] if i % 2 != 0 else b11[0])(i))
	for i in range(3):
		print_there(x0 + i * 5 + 12, 4, (lambda z: b8[0] if i % 2 == 0 else b12[1])(i))


def help_paint():
	"""paint border for help menu"""
	print_there(0, 1, yellow_note*80)
	print_there(0, 24, yellow_note * 80)
	for i in range(24):
		print_there(0, i, yellow_note)
		print_there(80, i, yellow_note)
