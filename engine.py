import os
import sys
import termios
import threading
import random
from time import sleep, time
from select import select
from operator import attrgetter
from functools import partial
from abc import ABCMeta, abstractmethod

import levels
from graphics import (
	print_there, paint_barlines, preliminaries, paint_explosion,
	draw_moving_object, draw_lift, borders_monster, fizzle
)
from resources import *


class StoppableThread(threading.Thread):
	"""Threading Subclass to enable to pause and stop by using appropriate methods and attributes"""
	pause = threading.Event()
	restart = 0

	def __init__(self, *args, **kwargs):
		super(StoppableThread, self).__init__(*args,  **kwargs)

	@classmethod
	def launch(cls):
		cls.pause.set()

	@classmethod
	def stop(cls):
		cls.pause.clear()


def threads(fn):
	"""Threads decorator function, functions decorated with it start as threads-daemons"""
	def wrapper(*args,  **kwargs):
		t = StoppableThread(target=fn, args=args, kwargs=kwargs)
		t.daemon = True
		t.start()
	return wrapper


def is_data():
	"""Wait the data in the stdin: literally - wait 0 to read from sys.stdin"""
	return select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])


def get_key(pause=0):
	"""Non-blocking input, dynamically reading one symbol from user: basically, it loops 3 times and returns if nothing
	to read from buffer, if there is something, first if key_code is Enter or another key (see inline comment below)
	it returns it to main cycle	if it equals '27' it may be Esc or arrows, to determine it, stdin_counter var is used:
		1. stdin_counter is incremented each time there is data to read from stdin buffer
		2. Esc has an ord of '27' the problem is that arrows  keys code also start with this code,
		but they contain 3 symbols:	for instance [27,91,68] for left arrow, so to distinct between them our function:
		3. checks the stdin_counter, if within 0.2s the latter equals 3 and stdin-buffer starts with 27 then it's arrow,
		4. if stdin_counter equals 1 and during 0.2s nothing was passed to stdin then it's Esc
		5. else return None or simply another key_code specified in list"""
	counter = 0
	stdin_counter = 0
	start_stdin = 0
	while counter < 3:
		if is_data():
			stdin_counter += 1
			if stdin_counter == 1:
				start_stdin = time()
			answer = ord(os.read(sys.stdin.fileno(), 1))
			sys.stdout.flush()
			# to avoid keyboard freezing when during PAUSE arrows are pressed
			if pause == 1:
				stdin_counter = 1
		if answer in [10, 32, 80, 112, 81]:   # ' ', Enter, 'P', 'p', 'Q'
			return answer
		elif stdin_counter == 1 and answer == 27:
			if time() - start_stdin > 0.2:
				return answer   # 27 'Esc'
		elif stdin_counter == 3 and time() - start_stdin < 0.2:
			return answer  # arrows
		else:
			counter += 1
	return None


def falling_obj(x, y, obj, bricks=None, i=None, speed=0.1, prize=0):
	"""Standalone function to handle common patterns when prizes are falling, bomb dropped or fire shot
	Until reached the paddle keep falling/being redrawn"""
	while y < 21:
		draw_moving_object(x+1, y+2, obj, StoppableThread.pause, speed=speed)
		if StoppableThread.restart:
			return None
		y += 1
		if prize:
			# redraw the bricks through which the prizes are falling
			# without it the falling objects leave black trace behind - so redraw
			if y <= (y_dim + 1) and (bricks[i].endurance > 0 or bricks[i].status == 'E'):
				print_there(x, y, bricks[i].color)
			i += 12
	return 1


class Paddle:
	final_barline = 0

	def __init__(self, current_level, position=24, length=10, lives=5):
		"""Everything is straightforward, only for boss level special logic is needed: fire is ON"""
		self.length = length
		self.lives = lives
		self.position = position
		self.auto = 0
		self.glue = 0
		self.protection = 0
		self.glue_lock = threading.Event()
		self.glue_lock.clear()
		if current_level not in boss_levels:
			self.fire_mode = 0
		else:
			self.fire_mode = 1
		self.paint()

	def move(self, direction):
		"""Left/Right moving before redrawing, depends on position of the paddle in order not to cross the borders"""
		if self.auto > 0:
			return
		StoppableThread.pause.wait()
		if direction < 0 and self.position >= 4:
			self.position += direction
		elif direction > 0 and self.length + self.position <= 61:
			self.position += direction

	@threads
	def autopilot(self, ball_launch, prizes_level, monster, matrix, lift, *bricks):
		"""autopilot thread, it tracks the first balls in Ball.balls list
		it works several seconds, decreasing its value until 0"""
		boss = None  # No boss on common levels
		self.auto = 1000
		if self.glue != 0:
			self.glue_lock.set()
		d_ = self.glue, self.protection      # saving paddle attributes
		self.glue = 0
		self.protection = 999                # quasi invulnerability during autopilot
		s = time()
		while self.auto > 0:
			StoppableThread.pause.wait()
			if StoppableThread.restart == 1:
				return
			if self.auto < 20:
				print_there(self.position, 23, BLANK * (self.length+1))
				sleep(Ball.speed/6)
			if self.fire_mode > 0:
				if time() - s > 0.35:    # if fire_mode is on then fire
					self.fire_daemon(ball_launch, prizes_level, monster, matrix, lift, boss, *bricks)
					s = time()
			try:                                # if no balls left return even if autopilot is caught
				x = Ball.balls[0].x             # autopilot follows only one ball - first in the Ball.balls list
			except IndexError:
				self.auto = 0
				break
			center = self.position + self.length // 2
			if x not in range(center - 2, center + 2):
				if center > x and self.position > 3:
					direction = -1
				elif center < x and self.length + self.position <= 60:
					direction = 1
				else:
					direction = 0
				self.position += direction
				self.paint(direction)
			sleep(Ball.speed/6)
			self.auto -= 1
		self.glue, self.protection = d_     # loading paddle attributes
		if self.glue != 0:
			self.glue_lock.clear()
		print_there(2, 23, BLANK * 61)
		if self.position % 2 != 0:
			self.position += 1
		self.paint()

	def bomb_collision(self, x):
		"""Protection-- or if the latter equals 0 Lives-- and call paint the explosion function"""
		if self.protection != 0:
			self.protection -= 1
		else:
			self.lives -= 1
		self.paint(x_=x)

	def paint(self, direction=0, boss=0, x_=0):
		"""Draw/redraw the paddle or boss - it depends on prizes caught, but always track the actual size and
		watches that it does not cross the borders"""
		# -----------------by default---------------------------------------- #
		protection_pic = ''
		auto_pic = ''
		glue_layer = ''
		fire_pic = ''
		l_auto = 0
		y = 23
		len_ = 0
		boss_texture = ''
		if boss != 0:
			self.fire_mode = 0
			y = 2
			boss_texture = BOSS_
		elif boss == 0:
			print_there(64, y, LIVES * self.lives + (15 - self.lives) * BLANK)        # Redraw  Lives
			if self.protection != 0:
				if self.protection > 1:
					protection_pic = PROTECTION[1]
				elif self.protection == 1:
					protection_pic = PROTECTION[0]
				len_ += 1
			if self.auto != 0:
				auto_pic = AUTO_
				len_ += 1
			l_auto = len(auto_pic)
			if self.glue == 1:
				glue_layer = glue_color
				len_ += 1
			if self.fire_mode == 1:
				fire_pic = PIANO_FIRE
				len_ += 1
		x = self.position
		# blank paddle + one additional blank to assure clarity if not near border
		print_there(
			x - direction, y, BLANK * (self.length + l_auto + 1)
			+ (lambda z: '' if (x + self.length + len_) >= 61 else BLANK)(x))
		if not boss and self.auto != 0:
			print_there(x, y, auto_pic + boss_texture + PIANO * (self.length-len_) + protection_pic)
		else:
			print_there(x, y, glue_layer + fire_pic + boss_texture + PIANO * (self.length-len_) + protection_pic)
		if x_ != 0:
			y = (lambda z: 22 if y == 23 else 3)(y)
			paint_explosion(x_, y)

	@threads
	def fire_daemon(self, ball_launch, prizes_level, monster, matrix, lift, boss, *bricks):
		"""Fire-mode, if lift is reached, continue from another lift, if monster is hit, the latter is exploded
		the shot is dissipated, when brick is shot - its endurance decreases"""
		x = self.position + int(self.length / 2)
		y = 21
		while y >= 1:
			if lift:       # if lift -then laser shot automatically transported to another lift
				if x in range(lift[0][0] - 1, lift[0][0] + 2) and y == (lift[0][1]) + 1:
					x = lift[1][0]
					y = lift[1][1] - 1
				elif x in range(lift[1][0] - 1, lift[1][0] + 2) and y == (lift[1][1]) + 1:
					x = lift[0][0]
					y = lift[0][1] - 1
			if (x in range(monster.x - 1, monster.x + 2)) and y == monster.y and 3 < monster.x < 60:  # monsters on screen
				monster.status = 'Explosion'
				return
			if boss and y == 2 and boss.position <= x <= boss.position + boss.length:
				boss.hp -= 3
				boss.paint_boss()
				paint_explosion(x, y+1)
				return
			if y <= y_dim + 2 and matrix[y-1, x] != 0:
				destroy_brick(x, y, self, bricks, prizes_level, ball_launch, monster, matrix, lift, i=0, j=-1)
				return
			draw_moving_object(x, y, TRILL, StoppableThread.pause, speed=0.05, b=1)
			y -= 1
			if StoppableThread.restart:
				return

	@classmethod
	@threads
	def barline(cls, b_):
		"""if barline prize is caught, this thread does not let the ball to drop for a certain time"""
		Paddle.final_barline = 100
		paint_barlines()   # paint barlines
		while Paddle.final_barline > 0:
			StoppableThread.pause.wait()
			if StoppableThread.restart:
				Paddle.final_barline = 0
				break
			if Paddle.final_barline < 5:
				print_there(0, 62, BLANK * 65)
				sleep(0.1)
				paint_barlines()
				Ball.ball_set_speed(b_)
			sleep(0.1)
			Paddle.final_barline -= 1
		print_there(0, 62, BLANK * 65)   # clear barlines


class Boss:
	__metaclass__ = ABCMeta

	def __init__(self, position, length, hp):
		self.length = length
		self.hp = hp
		self.position = position

	@abstractmethod
	def paint_boss(self):
		"""Every boss should have this method"""
		pass


class Boss1(Boss, Paddle):
	def __init__(self, position, length, hp):
		Boss.__init__(self, position, length, hp)

	@threads
	def boss_fireball(self, paddle,):
		"""Process boss' fire, basically as the rest of falling objects"""
		while True:
			if StoppableThread.restart:
				return
			sleep(random.uniform(0.5, 0.9))
			y = 3
			x = random.randint(self.position+1, self.position+self.length-1)
			if falling_obj(x, y, BOSS_FIRE, speed=0.04):
				if paddle.position < x < paddle.position + paddle.length - 1:
					paddle.bomb_collision(x)

	def paint_boss(self):
		"""Draws long(60) line consisting of the red_notes representing boss lives, each shot -= 2 points"""
		x = self.position
		print_there(x, 2, (BOSS_ + PIANO) * self.length)
		print_there(0, 0, BASS_CLEF + MUSICAL_STAFF * 60 + BASS_CLEF)
		print_there(2, 1, BOSS_LIVES * self.hp)

	@threads
	def boss_paddle(self):
		"""quasi-random wandering boss-paddle"""
		while True:
			t = 0
			z = random.randint(5, 45)
			while t < 10:
				t += 1
				if StoppableThread.restart:
					return
				StoppableThread.pause.wait()
				if self.hp <= 0:
					sleep(0.5)
					for _ in range(9):
						obj = (EXPLOSION[1] + BLANK) * ((self.length // 2) - 1)
						draw_moving_object(self.position-1, 3, obj, StoppableThread.pause, b=20)
						obj = BLANK + (EXPLOSION[0] + BLANK) * ((self.length // 2) - 1)
						draw_moving_object(self.position-1, 3, obj, StoppableThread.pause, b=20)
					return
				sleep(random.uniform(0.1, 0.2))
			while self.position != z and self.hp > 0:
				StoppableThread.pause.wait()
				if StoppableThread.restart:
					return
				if z - self.position > 0:
					direction = 1
				else:
					direction = -1
				self.position += direction
				Paddle.paint(self, boss=1, direction=direction)
				sleep(0.1)
				# to exit from while-loop immediately
				if self.hp < 0:
					break


# --------------------------------------------------Wandering bombs in boss level--------------------------------------#
@threads
def fireball_deamon(boss, paddle,):
	"""Quasi random wandering it flies 3 iteration at certain direction, than randomly changes it.
	If hits the paddle, then the latter loses one life. """
	x = 25
	y = 14
	i = 1
	j = -1
	q = 0
	while 2 < x + i < 60 and 2 < y + j < 24:
		if boss.hp <= 0:
			return
		if y == 22 and paddle.position <= x <= paddle.position + paddle.length - 1:
			paddle.bomb_collision(x)
			return
		if q == 3:
			i = [-1, 1][random.randrange(2)]
			j = [-1, 1][random.randrange(2)]
			q = 0
		draw_moving_object(x+i, y+j, (lambda z: BOMBS[0] if i > 0 else BOMBS[1])(i), StoppableThread.pause, speed=0.08, b=2)
		x += i
		y += j
		q += 1
		if StoppableThread.restart:
			return


# --------------------------------------------------Wandering enemies dropping bombs---------------------------------- #
class Monster:
	def __init__(self, paddle, current_level):
		"""Monsters are actually spawned by one thread, which starts by this method when monster obj is initialized"""
		self.x = 0
		self.y = 0
		self.status = ''
		self.threading = threading.Thread(target=self.monster_daemon, args=(paddle, current_level))
		self.threading.daemon = True
		self.threading.start()

	def stop_monster(self):
		"""When paddle has lost life you need to clear monsters"""
		self.status = 'Stopped'

	def monster_daemon(self, paddle, current_level):
		"""Main monster thread, loops until Esc is pressed or next level, it sleeps for (2,4)s in common levels
		and (0,2)s in boss levels, spawning monster which appears randomly from the left or from the right,
		moving along the horizontal line, then if not shot, sampling the one random x to drop bomb,
		then reaches the other side of the leve, disappears and then loops again"""
		while True:
			# randomly choose coordinate below bricks and at least 5-levels higher the paddle
			self.y = random.randint(y_dim + 2, 18)
			# open the borders
			if current_level not in boss_levels:
				# -----------------BOMB INTERVAL----------------------------------------------------------#
				rand_x = random.randint(7, 57)
			else:
				# -------- in boss levels incline to drop bombs near borders due to Fireballs-------------#
				rand_x = random.choice((random.randint(7, 27), random.randint(37, 57)))
			for _ in range(1000*(random.randint(0, 2)+(lambda z: 0 if current_level in boss_levels else 4)(current_level))):
				StoppableThread.pause.wait()
				if StoppableThread.restart:
					return
				sleep(0.001)
			# erase 2 random elements from borders to let the monster slipping through
			borders_monster(self.y, mode=0)
			sleep(0.5)
			# ---------------------direction of monster's movement----------------------------------------#
			self.x = random.choice([1, 61])
			direction = (lambda z: 1 if self.x == 1 else -1)(self.x)
			# choose type of monster. lambda because Snake-monster should not be moving from left to right
			type_ = (lambda z: random.randint(0, 3) if direction < 0 else random.randint(1, 3))(direction)
			self.status = ''
			while 0 < self.x < 62:
				if self.status == 'Explosion' or self.status == 'Stopped' or StoppableThread.restart == 1:
					paint_explosion(self.x, self.y, rate=0.2)
					self.x = 0
					sleep(0.3)
					break
				self.x += direction
				# --- draw monster -------------- #
				draw_moving_object(self.x, self.y, monsters[type_], StoppableThread.pause, speed=0.05, b=2)
				# --- bomb if necessary x-coordiante is reached --- #
				if self.x == rand_x:
					self.threading = threading.Thread(target=self.monster_bomb_daemon, args=(paddle, rand_x, self.y, type_,))
					self.threading.daemon = True
					self.threading.start()
			sleep(0.2)
			# restore borders
			borders_monster(self.y, mode=1)

	def monster_bomb_daemon(self, paddle, rand_x, y, type_,):
		"""Dropped bomb's thread - just common falling object, if hits the paddle then whips away one protection point
		if there are any, if not - then it deprives you with one live"""
		# choose corresponding bomb type
		bomb_type = [0, 1, 2][random.randrange(3)] if type_ < 2 else [3, 4, 5][random.randrange(3)]
		if falling_obj(rand_x, y, BOMBS[bomb_type]):
			if paddle.position <= rand_x <= paddle.position + paddle.length - 1:
				if self.status == 'Stopped':
					return
				paddle.bomb_collision(rand_x)


class Prize:
	falling = 0
	prizes_types = [
		SURPRISE,        # 1
		EXTEND,          # 2
		SHRINK,
		NEW_BALL,
		GLUE,            # 5
		FASTER,
		SLOWER,
		PROTECTION[1],   # 8
		DEATH_1,
		DEATH_2,
		EXTRA_LIFE,      # 11
		BARLINE,
		AUTOPILOT,
		FIRE,            # 14
					]

	def __init__(self, i, x, y, paddle, bricks, prizes_level, obj_num, ball_launch, monster, matrix, lift):
		"""Simply start daemon of the falling prize"""
		self.brick_number = obj_num
		self.prize_type = Prize.prizes_types[i-1]
		self.prize_x = x
		self.prize_y = y
		self.threading = threading.Thread(target=self.prize, args=(
								self.prize_x, self.prize_y, paddle, bricks,
								prizes_level, ball_launch, monster, matrix, lift))
		self.threading.daemon = True
		self.threading.start()

	def prize(self, x, y, paddle, bricks, prizes_level, ball_launch, monster, matrix, lift):
		"""This method-daemon handles falling prizes: choose the reward accordingly, in case of the Surprise prize
		the probabilities differ for different prizes. There are several caveats for certain prizes:
		see the inline comments below"""
		i = self.brick_number
		Prize.falling += 1
		if falling_obj(x, y, self.prize_type, bricks, i, speed=0.18, prize=1):
			# if prize is caught
			if paddle.position - 1 <= x + 2 <= paddle.position + paddle.length:
				if self.prize_type == Prize.prizes_types[0]:                    # Surprise
					a = random.randint(0, 99)
					if a in [98, 99]:         # Fire less probable
						self.prize_type = Prize.prizes_types[12]
					elif a in [96, 97]:        # Death less probable
						self.prize_type = Prize.prizes_types[8]  # or [9]
					elif a in [list(range(90, 96))]:   # Autopilot slightly less probable
						self.prize_type = Prize.prizes_types[11]
					elif a in [list(range(84, 90))]:   # Barlines slightly less probable
						self.prize_type = Prize.prizes_types[11]
					elif a in [list(range(78, 84))]:    # Life++ slightly less probable
						self.prize_type = Prize.prizes_types[10]
					elif a in [list(range(72, 78))]:    # Glue slightly less probable
						self.prize_type = Prize.prizes_types[5]
					else:
						self.prize_type = Prize.prizes_types[a % 6 + 1]
				if self.prize_type == Prize.prizes_types[1]:                    # Length+2
					if paddle.length < 16:
						if paddle.length + paddle.position >= 60:     # if not out of borders
							paddle.position -= 2
							paddle.length += 2
							paddle.paint(direction=2)
						else:
							paddle.length += 2
							paddle.paint()
				elif self.prize_type == Prize.prizes_types[2]:                  # Length-2
					if paddle.length >= 6:
						paddle.length -= 2
						paddle.paint(direction=-2)
				elif self.prize_type == Prize.prizes_types[3]:                  # Ball++
					ball = Ball(x+2, status=1)
					ball.ball_display(bricks, prizes_level, paddle, ball_launch, monster, matrix, lift)
				elif self.prize_type == Prize.prizes_types[4]:                  # Glue
					if paddle.glue != 1:
						paddle.glue = 1
						paddle.glue_lock = threading.Event()
						paddle.glue_lock.clear()
						paddle.paint()
				elif self.prize_type == Prize.prizes_types[5]:                  # Faster Cresc.
					if Ball.speed > 0.0375:
						Ball.ball_set_speed(Ball.speed - 0.03)
				elif self.prize_type == Prize.prizes_types[6]:                  # Slower Dimin.
					if Ball.speed < 0.15 and Paddle.final_barline == 0:
						Ball.ball_set_speed(Ball.speed + 0.04)
				elif self.prize_type == Prize.prizes_types[7]:                  # Protection
					paddle.protection += 1
					paddle.paint()
				elif self.prize_type == Prize.prizes_types[8] or self.prize_type == Prize.prizes_types[9]:  # Death
					paddle.bomb_collision(x)
				elif self.prize_type == Prize.prizes_types[10]:                 # Life++
					if paddle.lives < 9:
						paddle.lives += 1
						paddle.paint()
				elif self.prize_type == Prize.prizes_types[11]:                 # Barlines
					b_ = Ball.speed
					Ball.ball_set_speed(0.03)
					if Paddle.final_barline != 0:
						Paddle.final_barline = 100
					else:
						Paddle.barline(b_)
				elif self.prize_type == Prize.prizes_types[12]:                 # AUTOPILOT
					if paddle.auto != 0:
						paddle.auto = 1000
					else:
						paddle.autopilot(ball_launch, prizes_level, monster, matrix, lift, *bricks)
				elif self.prize_type == Prize.prizes_types[13]:                 # Fire
					paddle.fire_mode = 1
					paddle.paint()
		# to avoid 'no_balls' or immediate next_level conditions in the main loop
		sleep(0.3)
		Prize.falling -= 1


class Bricks:
	d = {}

	def __init__(self, i, prizes_level):
		"""Bricks are initialized according to its endurance and type. There are 3 classes of them: common,
		indestructible and blinking. Only the first ones are added to Bricks dictionary and its length determines
		whether level is cleared"""
		self.endurance = level[i][-1]  # endurance is always the last element in bricks[list] in resources
		#  for non-empty bricks
		if self.endurance != 0:
			self.color = level[i][self.endurance-1]
		else:     # vacuum
			self.color = ''
		if self.endurance > 0 and level[i][-2] != 'B':
			self.status = 'ON'
			Bricks.d[i] = 'ON'
		elif level[i][-2] == 'B':
			self.status = 'B'
		else:
			self.status = 'E'   # everlasting
		self.number = i
		self.prize = prizes_level[i]

	def paint_bricks(self, paddle, bricks, prizes_level, ball_launch, monster, matrix, lift=None, i=0, x=0, y=0, delete=0):
		"""Called on creation of bricks if delete argument == 0 or to erase / decrement endurance if delete == 1 """
		# ------------if creation -------------------------#
		if delete == 0:
			x = (i % 12) * 5 + 2
			y = i // 12 + 2
		# ------------ if destruction ---------------------#
		if delete != 0:
			if self.endurance <= 0:
				return
			# decrement endurance in endurance matrix
			for s in range(5):
				matrix[y, x + s] = matrix[y, x + s] - 1
			self.endurance -= 1
			self.color = level[i][self.endurance - 1]
			# if brick's endurance is zero (or below) and if it is not blinking check whether there is prize in it
			if self.endurance <= 0 and level[i][-2] != 'B':
				self.status = 'OFF'
				if self.prize != 0:
					# if there is prize  - than initialize and launch prize daemon
					prizes_level[i] = Prize(
						self.prize, x, y-1, paddle, bricks, prizes_level,
						i, ball_launch, monster, matrix, lift,
					)
					self.prize = 0
				# in order to assure to wait the falling prize in the main loop until game is switched to the next level
				if len(Bricks.d) == 1 and self.prize != 0:
					sleep(0.5)
				del Bricks.d[i]
			if self.endurance == 0 and self.status == 'B':
				self.threading_blink(paddle, bricks, prizes_level, ball_launch, monster, matrix, lift, i, x, y)
		print_there(x, y, (lambda z: BLANK * 5 if self.endurance == 0 else self.color)(self.endurance))

	@threads
	def threading_blink(self, paddle, bricks, prizes_level, ball_launch, monster, matrix, lift, i, x, y):
		"""Thread to restore the blinking bricks after the 7s"""
		for _ in range(7000):
			if StoppableThread.restart:
				# if Esc or no balls - then redraw and restore immediately
				break
			StoppableThread.pause.wait()
			sleep(0.001)
		self.__init__(i, prizes_level)
		# in order to be assured that no balls in vicinity, otherwise endurance matrix can be convoluted
		# if ball is in the brick place exactly when matrix is regenerated
		while True:
			for ball in Ball.balls:
				if x - 3 < ball.x < x + 8 and y - 2 < ball.y < y + 2:
					break
			else:
				# restore endurance Matrix for this blinking brick
				for s in range(5):
					matrix[y, x + s] = matrix[y, x + s] + 1
				self.paint_bricks(paddle, bricks, prizes_level, ball_launch, monster, matrix, lift, i)
				return


def destroy_brick(x, y, paddle, bricks, prizes_level, ball_launch, monster, matrix, lift, i=0, j=0):
	"""Standalone function to pass the necessary arguments to paint_bricks method in order to destroy the brick """
	obj_num = (y - 2 + j) * 12 + abs(x - 2 + i) // 5
	if 0 <= obj_num < 12 * y_dim:
		bricks[obj_num].paint_bricks(
			paddle, bricks, prizes_level, ball_launch, monster, matrix, lift,
			x=((abs(x - 2 + i) // 5) * 5 + 2), y=y + j, i=obj_num, delete=1)


class Ball:
	speed = 0.15
	balls = []

	def __init__(self, x=29, status=0, mode=0):
		self.x = x           # paddle_position + paddle_length//2
		self.y = 22
		self.status = status
		if mode == 1:          # first new ball
			Ball.balls = []
			Ball.ball_set_speed(0.12)
		Ball.balls.append(self)

	def paint_ball(self, paddle, direction=0):
		"""When unlaunched ball on moving paddle"""
		if (direction <= 0 and paddle.position >= 3) or (direction > 0 and ((paddle.length + paddle.position) <= 61)):
			print_there(self.x, self.y, BLANK)
			self.x += direction
			print_there(self.x, self.y, BALL)

	@classmethod
	def ball_set_speed(cls, speed):
		Ball.speed = speed

	@threads
	def ball_display(self, bricks, prizes_level, paddle, ball_launch, monster, matrix, lift):
		"""     Ball trajectory algorithm. Ball's path is determined by two coordinates x and y, which are changing
		depending on Ball.speed and angle each iteration. Direction is defined by two vars i and j:
		x coordinate: i == -1 ball is flying to the left elif i == 1 to the right
		y coordinate: j [-1,1] up, down
		There are 2 angles: angle_x and angle_y which determine the coordinates of corresponding axis at the next moment
		They can be both == 1, or either angle_x == 2 and angle_y == 1 or vice versa. For instance if angle_x == 2 and
		current x and y (10,20)  and i == 1 and j == 1 then the next iteration they will equal (12, 21)
		-------------------------------------------------------------------------------------------------------------
			Now about algorithm: it is pretty simple. First, for the paddle cases ,everything is straightforward: if the
		ball hits the paddle, then rebounds, else drops. Then, each iteration algorithm checks whether ball will hit
		the brick in the immediate vicinity, i.e. x+i, y+j (i,j determine movement direction). If there is a brick, then
		endurance of this brick is decremented and ball will change direction.  The order of checking: first, check
		if there is a brick in the x direction , then y, then if the ball hits exactly the butt of the brick then
		it will rebound (angle = PI, or i=-i,j=-j see above)
			Only when there is no bricks in vicinity, then algorithm checks if there are 'something' taking angles into
		account (don't forget that i and j might have been changed in the vicinity cycle). If there is, program simply
		relocates the ball by ONE coordinate to the necessary direction (according to i and j) and then simply goes to
		the next iteration (continue) WITHOUT actually moving the ball (because otherwise it will be painted inside the
		bricks instead of smashing it and this is certainly not what you want. Then, during the next iteration
		algorithm correctly destroys that brick, because now it is in direct vicinity.
		-------------------------------------------------------------------------------------------------------------
			About endurance matrix: each level has its own. It is built according to bricks being used. Each brick has
		length of 5 and height of 1 and is determined in levels.py module by Python list like that:
		[PIC_1 (when endurance == 1), PIC_2 (when endurance == 2), 2]
		The initial value in endurance matrix is written according to brick[endurance - 1] formula, then 5 values of 2(
		5 because each brick has length of 5) and this value is decreased when ball (x,y) hits it. Using x and y
		in the function destroy_brick and then Brick.paint_brick bricks endurance and images are changed correspondingly
		-------------------------------------------------------------------------------------------------------------
			The important point: all borders(except the lower one where the paddle resides) are conceptualized as
		being constructed with indestructible bricks, so NO additional checks are needed on borders."""
		# directions for x and y; right, up by default
		i = 1
		j = -1
		# angles: 45* by default, can be changed by collision with monsters
		angle_x = 1
		angle_y = 1
		while True:
			ball_launch.wait()                        # wait 'ball_launch' event
			if self.status == 0:                      # if not launched
				self.status = 1                       # launched
			if self.status == 2 or StoppableThread.restart:   # Esc is pressed - restart
				print_there(self.x, self.y, BLANK)
				return
			if self.x == 2:
				i = 1
			if self.x == 61:
				i = -1
			draw_moving_object(self.x, self.y, BALL, StoppableThread.pause, speed=Ball.speed, b=1)
			# --------------------------------------Collision with monster---------------------------------------------#
			if 3 <= monster.x <= 60 and monster.status != 'Explosion':   # monsters appear on the screen
				b_x = [self.x, self.x + i, self.x]
				m_x = [monster.x - 1, monster.x, monster.x + 1]
				b_y = [self.y, self.y+j]
				m_y = [monster.y - 1, monster.y, monster.y + 1]
				if any(i in b_x for i in m_x) and any(i in b_y for i in m_y):
					monster.status = 'Explosion'
					# --- Randomly change direction and angles of the ball --- #
					i = [-1, 1][random.randrange(2)]
					j = [-1, 1][random.randrange(2)]
					angle_x = [1, 2][random.randrange(2)]
					if angle_x == 1:
						angle_y = [1, 2][random.randrange(2)]
					elif angle_x == 2:
						angle_y = 1
			# -------------------------------------------Lift--------------------------------------------------------- #
			if lift:
				if self.x == lift[0][0] or self.x == lift[1][0] and self.y == lift[0][1] or self.y == lift[1][1]:
					draw_lift(lift)    # redraw lift in case of direct collision with ball
				if self.x in range(lift[0][0]-1, lift[0][0]+2) and self.y in range(lift[0][1]-1, lift[0][1]+2):
					self.x = lift[1][0] + i
					self.y = lift[1][1] + j
				elif self.x in range(lift[1][0]-1, lift[1][0]+2) and self.y in range(lift[1][1]-1, lift[1][1]+2):
					self.x = lift[0][0] + i
					self.y = lift[0][1] + j
			# -------------------------------------------------------------------------------------------------------- #
			# ---------------------------------------------ALGORITHM-------------------------------------------------- #
			# ------------------------------------------------ paddle  cases-------------------------------------------#
			# First handle cases when ball is about to drop, first, if prize barlines is taken, then it will prevent the
			# ball from falling for a certain time. 2nd: if ball's coordinates do not belong to paddle.position +
			# + paddle.length, then remove ball from Ball.balls list and return. Else, the ball will rebound (180*)
			# from the paddle's butt if it flies from appropriate direction right to the ends of the paddle.
			# Else it'll simply changes the y direction vector and fly up.
			if (self.y + j * angle_y) > 22:
				p = paddle.position + paddle.length
				if Paddle.final_barline > 0:    # barlines prize is taken
					j = -j
					continue
				# to handle situations when angle_y > 1 and ball should approach a bit (+j) to reach necessary y to land
				if angle_y == 2 and self.y == 21:
					self.x, self.y = self.square_diagonal(i, j)
				if paddle.position - 1 <= self.x <= p + 1:
					j = -j
					if (i > 0 and self.x > 3 and self.x + 1 in [paddle.position, paddle.position + 1]) or (
						i < 0 and self.x < 60 and self.x - 1 in [p-1, p]):
						# 180* rebound from paddle's butt, but not if near the borders
						i = -i
					if paddle.glue == 1:
						self.status = 0
						if self.x < paddle.position:
							self.x += 1
						elif self.x >= paddle.position + paddle.length:
							self.x -= 2
						print_there(self.x, self.y, BALL)
						paddle.glue_lock.wait()
						print_there(self.x, self.y, BLANK)
				else:
					self.square_diagonal(i, j)
					Ball.balls.remove(self)
					return
			#  Next moment: in vicinity, and angles == 1  ( angle_x == angle_y) FIRST WITHOUT ANGLES JUST CHECK VICINITY
			#  check whether at the next moment ball with vector (x,y) (i,j) hits bricks
			in_vicinity = 0                           # see below
			destructor = partial(destroy_brick, self.x, self.y, paddle, bricks, prizes_level, ball_launch, monster, matrix, lift)
			while True:
				# ----------------------------------------# nearby, vicinity  cases----------------------------------- #
				# --------------------------------- INDEXING OVERLOADED! index = index - 1 --------------------------- #
				if matrix[self.y, abs(self.x+i)] != 0:     # pure x
					if 2 < self.x < 60:   # not to delete bricks when ball strikes the borders
						destructor(i=i, j=0)
					i = -i
					in_vicinity = 1
				if matrix[self.y+j, self.x] != 0:          # pure y
					destructor(i=0, j=j)
					j = -j
					in_vicinity = 1
				if matrix[self.y+j, abs(self.x+i)] != 0:   # rebound, diagonal cases
					destructor(i=i, j=j)
					i = -i
					j = -j
					in_vicinity = 1
				if in_vicinity:
					in_vicinity = 0
				else:    # --- loop until in_vicinities == 0 for all x, y and diagonal
					break
			# ------------------------------------------ angle  cases------------------------------------------------- #
			if (angle_x != 1 or angle_y != 1) and matrix[self.y + j * angle_y, abs(self.x + i * angle_x)] != 0:
				self.x, self.y = self.square_diagonal(i, j)
				continue   # next iteration - let the vicinity cases care for now!
			# ---------------------Moving Ball at the next moment: change its coordinates----------------------------- #
			self.x += i * angle_x
			self.y += j * angle_y  # position of the ball in the next moment

	def square_diagonal(self, i, j):
		self.x += i
		self.y += j
		draw_moving_object(self.x, self.y, BALL, StoppableThread.pause, speed=Ball.speed/4, b=1)
		return self.x, self.y


def moving_around(paddle, current_level, direction):
	if current_level not in boss_levels:
		# to avoid situations when 2 or more non-moving balls are shadowing each other after moving paddle & redrawing
		# (because of the last BLANK space that this function is drawing can erase the next ball
		# sorted if moving left - so the leftmost ball's redrawing function called first
		if direction < 0:
			s = False
		# and reversed if the opposite
		else:
			s = True
		for ball in sorted(Ball.balls, key=attrgetter('x'), reverse=s):
			if ball.status == 0:
				ball.paint_ball(paddle, direction)
	paddle.move(direction)
	paddle.paint(direction=direction)


def init_paddle(current_level, lives=5):
	"""routine to create and paint paddle"""
	# create paddle
	paddle = Paddle(current_level, lives=lives)
	# draw paddle
	paddle.paint()
	return paddle


def init_ball(bricks, prizes_level, paddle, ball_launch, monster, matrix, lift):
	"""routine to create and paint first ball in the beginning of the level or after no_balls_left"""
	# Create ball (x,y,speed)
	ball = Ball(mode=1)
	ball.paint_ball(paddle)
	# Launch ball daemon (x,y,speed)
	ball.ball_display(bricks, prizes_level, paddle, ball_launch, monster, matrix, lift)
	StoppableThread.launch()


def game_proc(current_level):
	"""main proc, here keyboard is processed and main game cycle is looping"""
	global level, y_dim
	lives = 4   # by default 4 lives
	while True:
		# endurance matrix, prizes matrix are determined in the levels.py module
		y_dim, matrix, level, prizes_level, lift = levels.choose_level(current_level)
		# draw borders, prizes names
		preliminaries(current_level)
		launched = 0
		pause = 0
		start = 0
		start_fireball = 0
		StoppableThread.restart = 0
		ball_launch = threading.Event()
		ball_launch.clear()
		paddle = init_paddle(current_level, lives)
		# monster init
		monster = Monster(paddle, current_level)
		# create bricks
		bricks = [Bricks(i, prizes_level) for i in range(12 * y_dim)]  # create bricks
		# draw bricks
		for i in range(12 * y_dim):
			sleep(0.0075)
			bricks[i].paint_bricks(paddle, bricks, prizes_level, ball_launch, monster, matrix,  i=i, delete=0)
		if current_level not in boss_levels:  # non-boss level
			boss = None
			init_ball(bricks, prizes_level, paddle, ball_launch, monster, matrix, lift)
			if lift:
				draw_lift(lift)
		else:
			# --- BOSS level --------------------------------------------------#
			boss = Boss1(24, 10, 60)         # init boss
			boss.paint_boss()                # paint boss
			boss.boss_fireball(paddle,)      # init boss_weapons
			boss.boss_paddle()               # draw boss paddle
			start_fireball = time()          # start fireballs after 1s
			StoppableThread.launch()
		# flush stdin in case some keys were pressed during NEW_LEVEL etc messages
		termios.tcflush(sys.stdin, termios.TCIOFLUSH)
		while True:
			if is_data():
				answer = get_key(pause)
				if answer == 32:  # SPACE
					if not pause:
						if paddle.glue == 1:
							paddle.glue_lock.set()
							paddle.glue_lock.clear()
						if current_level not in boss_levels:
							ball_launch.set()
						if paddle.fire_mode == 1 and paddle.auto == 0:
							if launched != 0:
								if time() - start > 0.5:
									paddle.fire_daemon(ball_launch, prizes_level, monster, matrix, lift, boss, *bricks)
									start = time()
							else:
								launched = 1
								start = time()
								paddle.fire_daemon(ball_launch, prizes_level, monster, matrix, lift, boss, *bricks)
						else:
							launched = 0
					continue
				# non-arrows were passed
				if answer == 27:                               # '\x1b 'Esc'
					if not pause:
						StoppableThread.restart = 1
				if answer == 112 or answer == 80:              # 'p', 'P'
					if pause == 0:
						StoppableThread.stop()
						pause = 1
					else:
						StoppableThread.launch()
						pause = 0
				if answer == 81:                              # 'Q'
					if pause == 0:    # not while PAUSE
						sys.exit()
				# -----------  arrows ----------- #
				if answer == 68:                              # left arrow
					moving_around(paddle, current_level, direction=-2)
				elif answer == 67:                            # right arrow
					moving_around(paddle, current_level, direction=2)
			if boss:
				if time() - start_fireball > 1 and not pause:
					if threading.active_count() < 10:
						fireball_deamon(boss, paddle)
						start_fireball = time()
				# BOSS level cleared
				if boss.hp <= 0:
					sleep(1)
					monster.stop_monster()
					StoppableThread.restart = 1
					sleep(3)
					break
			# --- GAME OVER to menu ------------------------------ #
			if paddle.lives <= 0:
				StoppableThread.restart = 1
				fizzle(game_over_font)
				print_there(35, 12, GAME_OVER)
				sleep(2)
				# clear left bricks
				Bricks.d = {}
				return    # return to menu
			# --- Non-boss level cleared ------------------------- #
			if not Prize.falling and not boss and len(Bricks.d) == 0:
					StoppableThread.restart = 1
					print_there(11, 12, NEW_LEVEL)
					sleep(4)
					break
			# -----------------------No balls left or Esc ---------------------------------------------#
			# if escape is pressed, level is restarted, but current state is preserved
			# OR if no balls left and no prizes are falling and non-boss level
			if (len(Ball.balls) == 0 and not Prize.falling and not boss) or StoppableThread.restart:
				monster.stop_monster()
				StoppableThread.restart = 1
				print_there(2, 22, BLANK * 60)
				while paddle.length > 0:
					paddle.length -= 1
					paddle.paint(direction=-1)
					sleep(0.05)
				print_there(2, 23, BLANK * 61)
				sleep(1)
				paddle.lives -= 1
				paddle = init_paddle(current_level, paddle.lives)
				StoppableThread.restart = 0
				monster = Monster(paddle, current_level)
				if boss:
					print_there(2, 2, BLANK * 60)
					boss = Boss1(24, 10, 60, )  # init boss
					boss.paint_boss()  # paint boss
					boss.boss_fireball(paddle, )  # init boss_weapons
					boss.boss_paddle()  # draw boss paddle
					start_fireball = time()
				else:
					# --- clear non-moving balls --- #
					for ball in Ball.balls:
						ball.status = 2
						Ball.balls.remove(ball)
					ball_launch.clear()
					init_ball(bricks, prizes_level, paddle, ball_launch, monster, matrix, lift)
				# flush stdin
				termios.tcflush(sys.stdin, termios.TCIOFLUSH)
	# ------------------------------------------LEVEL CLEARED---------------------------------------------#
		if current_level not in boss_levels:
				Ball.balls = []
				Ball.ball_set_speed(0.1)
				print_there(2, 23, BLANK * 60)
				lives = paddle.lives
				current_level += 1
		else:
			fizzle(green_note)
			print_there(23, 10, COMPLETE_VICTORY)   # if it was BOSS level
			print_there(31, 12, ENTER_TO_MENU)
			# flush stdin
			termios.tcflush(sys.stdin, termios.TCIOFLUSH)
			while not is_data():
				pass
			return
