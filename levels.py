import random

from resources import *


#  ------------------------------level_1--------------------------------------------------------
def level_1_init():
	""" All levels are constructed using list comprehensions with bricks defined in the resources.py module
	Each brick has its own endurance and pic, see ball_display function in engine.py for more details
	y_dim -  each level has certain layers which should be filled with bricks (it may be empty brick with 0 endurance)
	For example for this level there 7 of them. Next, list comprehension to build the level's bricks
		Prizes_level_x defines whether each particular brick has a prize, each number corresponds to one prize, see
	engine.py to determine that number.
		Then endurance matrix is compose according to each brick's endurance"""
	lift = None
	y_dim = 7
	level_1 = [[b1, b2][i % 2] if (i//12) % 2 == 0 else [b3, b2][(i-1) % 2] for i in range(12*y_dim)]
	prizes_level_1 = [0 for x in range(12*y_dim)]
	for i in range(6):
		prizes_level_1[i*12+1] = 7
		prizes_level_1[i*12+11] = 2
		prizes_level_1[i*12+2] = 3
		prizes_level_1[i*12+10] = 2
		prizes_level_1[i*12+4] = 3
		prizes_level_1[i*12+5] = 6
	for i in random.sample(range(1, 12*y_dim), 5):
		prizes_level_1[i] = 1
	for i in random.sample(range(1, 12*y_dim), 5):
		prizes_level_1[i] = 8
	prizes_level_1[0] = 11;  prizes_level_1[80] = 11; prizes_level_1[5] = 11   # Life++
	prizes_level_1[26] = 2
	prizes_level_1[52] = 2
	prizes_level_1[45] = 4
	prizes_level_1[72] = 4
	prizes_level_1[73] = 4
	prizes_level_1[82] = 4
	prizes_level_1[83] = 4
	for i in random.sample(range(1, 12 * y_dim), 3):
		prizes_level_1[i] = 11
	prizes_level_1[83] = 14
	matrix = matrix_endurance(y_dim, level_1)
	matrix = SpecialList(matrix)
	return y_dim, matrix, level_1, prizes_level_1, lift


#  ------------------------------level_2--------------------------------------------------------
def level_2_init():
	lift = None
	y_dim = 8
	level_2 = [[b1, b2_0][i % 2] if (i//12) % 2 == 0 else [b1, b2_0][(i-1) % 2] for i in range(12*y_dim)]
	for i in range(26, 70, 12):
		level_2[i] = b102
	for i in range(33, 70, 12):
		level_2[i] = b102
	prizes_level_2 = [0 for x in range(12*y_dim)]
	for i in range(8):
		prizes_level_2[i*12+1] = 2
		prizes_level_2[i*12+10] = 2
		prizes_level_2[i*12+3] = 3
		prizes_level_2[i*12+7] = 3
	prizes_level_2[25] = 3
	prizes_level_2[37] = 3
	prizes_level_2[70] = 3
	prizes_level_2[58] = 3
	prizes_level_2[84] = 4
	prizes_level_2[85] = 4
	prizes_level_2[94] = 4
	prizes_level_2[95] = 4
	prizes_level_2[93] = 12
	prizes_level_2[2] = 1
	prizes_level_2[9] = 1
	for i in random.sample(range(1, 12*y_dim), 5):
		prizes_level_2[i] = 8
	for i in random.sample(range(1, 12*y_dim), 10):
		prizes_level_2[i] = random.choice([12, 13])
	for i in random.sample(range(1, 12 * y_dim), 8):
		prizes_level_2[i] = 1
	for i in random.sample(range(1, 12 * y_dim), 2):
		prizes_level_2[i] = 11
	prizes_level_2[0] = 11; prizes_level_2[11] = 11; prizes_level_2[46] = 11   # Life++
	matrix = matrix_endurance(y_dim, level_2)
	matrix = SpecialList(matrix)
	return y_dim, matrix,  level_2, prizes_level_2, lift


#  ------------------------------level_3--------------------------------------------------------
def level_3_init():
	lift = None
	y_dim = 12
	level_3 = [b0 for _ in range(144)]
	for i in range(11):
		for j in range(i+1):
			level_3[i * 12 + j] = (lambda z: b7_ if (i+j) % 2 == 0 else b3)(i+j)
	for i in range(12):
		level_3[132+i] = b113
	level_3[11] = b11
	level_3[143] = b0
	prizes_level_3 = [0 for _ in range(12 * y_dim)]
	for i in random.sample(range(1, 12 * y_dim), 8):
		prizes_level_3[i] = 1
	for i in random.sample(range(1, 12 * y_dim), 8):
		prizes_level_3[i] = 8
	for i in random.sample(range(1, 12 * y_dim), 8):
		prizes_level_3[i] = 9
	for i in random.sample(range(1, 12 * y_dim), 8):
		prizes_level_3[i] = 10
	for i in random.sample(range(1, 12 * y_dim), 3):
		prizes_level_3[i] = 11
	prizes_level_3[72] = 5
	prizes_level_3[95] = 5
	prizes_level_3[100] = 5
	prizes_level_3[94] = 13
	prizes_level_3[11] = 14
	matrix = matrix_endurance(y_dim, level_3)
	matrix = SpecialList(matrix)
	return y_dim, matrix,  level_3, prizes_level_3, lift


#  ------------------------------level_4--------------------------------------------------------
def level_4_init():
	lift = None
	y_dim = 12
	level_4 = [[b3, b2][i % 2] if (i//12) % 2 == 0 else [b9, b8][(i-1) % 2] for i in range(12*y_dim)]
	for i in range(2):
		for j in range(3):
			level_4[132+j+i*9] = b110
	level_4[125] = b1
	level_4[126] = b1
	for i in range(3, 9):
		level_4[132+i] = b0
	prizes_level_4 = [0 for x in range(12*y_dim)]
	for i in range(10):
		prizes_level_4[random.randint(0, 140)] = 4
	for i in range(5):
		prizes_level_4[random.randint(0, 140)] = 6
	for i in range(5):
		prizes_level_4[random.randint(0, 140)] = 7
	for i in range(20):
		prizes_level_4[random.randint(0, 140)] = random.choice([1, 2, 3, 4])
	for i in range(10):
		prizes_level_4[random.randint(0, 140)] = random.choice([12, 13])
	for i in range(5):
		prizes_level_4[random.randint(0, 140)] = 8
	prizes_level_4[125] = 14; prizes_level_4[126] = 14; prizes_level_4[75] = 14; prizes_level_4[30] = 14
	prizes_level_4[random.randint(12, 120)] = 11; prizes_level_4[0] = 11;  prizes_level_4[11] = 11   # Life++
	matrix = matrix_endurance(y_dim, level_4)
	matrix = SpecialList(matrix)
	return y_dim, matrix,  level_4, prizes_level_4, lift


#  ------------------------------level_5--------------------------------------------------------
def level_5_init():
	lift = None
	y_dim = 12
	level_5 = [[b3, b8][i % 2] if (i//12) % 2 == 0 else [b10, b6][(i-1) % 2] for i in range(12*y_dim)]
	for i in range(12):
		level_5[i] = b0
		level_5[i+12] = b0
		level_5[i*12] = b0
		level_5[i*12-1] = b0
	prizes_level_5 = [0 for x in range(12 * y_dim)]
	for i in range(50):
		prizes_level_5[random.randint(0, 140)] = random.choice([1, 2, 3, 4, 6, 7, 8, 9, 10])
	for i in range(3):
		prizes_level_5[random.randint(0, 140)] = random.choice([12, 13])
	prizes_level_5[random.randint(12, 120)] = 11; prizes_level_5[0] = 11
	matrix = matrix_endurance(y_dim, level_5)
	matrix = SpecialList(matrix)
	return y_dim, matrix, level_5, prizes_level_5, lift


#  ------------------------------level_6--------------------------------------------------------
def level_6_init():
	lift = None
	y_dim = 12
	level_6 = [[b12, b13][i % 2] if (i//12) % 2 == 0 else [b1, b11][(i-1) % 2] for i in range(12*y_dim)]
	matrix = matrix_endurance(y_dim, level_6)
	matrix = SpecialList(matrix)
	prizes_level_6 = [0 for x in range(12 * y_dim)]
	for i in range(50):
		prizes_level_6[random.randint(0, 140)] = random.choice([1, 2, 3, 4, 6, 7, 8, 9, 10])
	for i in range(5):
		prizes_level_6[random.randint(0, 140)] = 6
	for i in range(3):
		prizes_level_6[random.randint(0, 140)] = 7
	for i in range(20):
		prizes_level_6[random.randint(0, 140)] = random.choice([1, 2, 3, 4])
	for i in range(5):
		prizes_level_6[random.randint(0, 140)] = random.choice([8, 12, 13])
	for i in range(5):
		prizes_level_6[random.randint(0, 140)] = 8
	for i in range(5):
		prizes_level_6[random.randint(0, 140)] = 5
	prizes_level_6[140] = 13
	prizes_level_6[125] = 14; prizes_level_6[132] = 14; prizes_level_6[23] = 14
	prizes_level_6[random.randint(12, 120)] = 11; prizes_level_6[0] = 11;  prizes_level_6[11] = 11   # Life++
	return y_dim, matrix, level_6, prizes_level_6, lift


# ------------------------------level_7--------------------------------------------------------
def level_7_init():
	lift = None
	y_dim = 13
	level_7 = [[b9, b11][i % 2] if (i//12) % 2 == 0 else [b8, b14][(i-1) % 2] for i in range(12*y_dim)]
	for j in range(3):
		for i in range(12):
			level_7[i+120+j*12] = b0
	for i in range(3):
		level_7[i*2 + 144] = b112
		level_7[i*2 + 151] = b112
	matrix = matrix_endurance(y_dim, level_7)
	matrix = SpecialList(matrix)
	prizes_level_7 = [0 for x in range(12 * y_dim)]
	for i in range(50):
		prizes_level_7[random.randint(0, 140)] = random.choice([1, 2, 3, 4, 6, 7, 8, 9, 10])
	for i in range(5):
		prizes_level_7[random.randint(0, 140)] = 6
	for i in range(5):
		prizes_level_7[random.randint(0, 140)] = 7
	for i in range(20):
		prizes_level_7[random.randint(0, 140)] = random.choice([1, 2, 3, 4])
	for i in range(15):
		prizes_level_7[random.randint(0, 140)] = random.choice([12, 13])
	for i in range(5):
		prizes_level_7[random.randint(0, 140)] = 8
	for i in range(3):
		prizes_level_7[random.randint(0, 140)] = 5
	for i in range(20):
		prizes_level_7[random.randint(0, 140)] = random.choice([9, 10])
	for i in range(7):
		prizes_level_7[random.randint(0, 140)] = 14   # life
	prizes_level_7[125] = 14; prizes_level_7[147] = 14; prizes_level_7[43] = 14
	prizes_level_7[random.randint(12, 120)] = 11; prizes_level_7[0] = 11;  prizes_level_7[11] = 11   # Life++
	return y_dim, matrix, level_7, prizes_level_7, lift


#  ------------------------------level_8--------------------------------------------------------
def level_8_init():
	lift = None
	y_dim = 12
	level_8 = [[b15, b16][i % 2] if (i//12) % 2 == 0 else [b15, b16][(i-1) % 2] for i in range(12*y_dim)]
	prizes_level_8 = [0 for x in range(12*y_dim)]
	for i in range(100):
		prizes_level_8[random.randint(0, 140)] = random.choice(list(range(1, 15)))
	for i in range(10):
		prizes_level_8[random.randint(0, 140)] = 4
	for i in range(30):
		prizes_level_8[random.randint(0, 140)] = random.choice([9, 10])
	for i in range(3):
		prizes_level_8[random.randint(137, 143)] = 11
	prizes_level_8[0] = 11;  prizes_level_8[44] = 11; prizes_level_8[11] = 11;     # Life++
	matrix = matrix_endurance(y_dim, level_8)
	matrix = SpecialList(matrix)
	return y_dim, matrix, level_8, prizes_level_8, lift


#  ------------------------------level_9--------------------------------------------------------
def level_9_init():
	lift = ((14, 4), (44, 6))
	y_dim = 13
	level_9 = [[b14, b2][i % 2] if (i//12) % 2 == 0 else [b3, b7][(i-1) % 2] for i in range(12*y_dim)]
	for i in range(7):
		level_9[5 + i] = b113
		level_9[101 + i] = b113
		level_9[17 + i*12] = b113
		level_9[23 + i*12] = b113
	for i in range(5):
		level_9[18 + i] = b2_01
		level_9[90 + i] = b2_01
		level_9[30 + i*12] = b2_01
		level_9[34 + i*12] = b2_01
	for j in range(5):
		for i in range(3):
			level_9[31+i + j*12] = b0
	for i in range(7):
		level_9[149+i] = b110
	for j in range(5):
		for i in range(3):
			level_9[1 + i + j*12] = b0
	matrix = matrix_endurance(y_dim, level_9)
	matrix = SpecialList(matrix)
	prizes_level_9 = [0 for x in range(12 * y_dim)]
	for i in range(50):
		prizes_level_9[random.randint(0, 140)] = random.choice(list(range(1, 15)))
	for i in range(4):
		prizes_level_9[random.randint(0, 155)] = random.choice([12, 13])
	for i in range(5):
		prizes_level_9[18 + i] = 11
	prizes_level_9[143] = 14; prizes_level_9[119] = 14
	prizes_level_9[24] = 11;  prizes_level_9[48] = 11    # Life++
	return y_dim, matrix, level_9, prizes_level_9, lift


#  ------------------------------level_10 BOSS--------------------------------------------------
def level_10_init():
	lift = None
	y_dim = 13
	level_10 = [b0 for i in range(12*y_dim)]
	matrix = matrix_endurance(y_dim, level_10)
	matrix = SpecialList(matrix)
	prizes_level_10 = [0 for x in range(12 * y_dim)]
	return y_dim, matrix, level_10, prizes_level_10, lift


#  ------------------------------general variables----------------------------------------------

class SpecialList(list):
	def __getitem__(self, index):
		y, x = index
		return super(SpecialList, self).__getitem__(y-1).__getitem__(x-1)

	def __setitem__(self, index, value):
		y, x = index
		super(SpecialList, self).__getitem__(y-1).__setitem__(x-1, value)


def matrix_endurance(y_dim, level):
	"""Endurance matrix is composed of 24 lists, however many there are actual bricks layers. Each list is filled
	 according to brick endurance, 0 if there is None brick on that position or when brick is smashed. Each border
	 except the lower one is represented by -1 which signifies invulnerability"""
	m = ([[] for _ in range(y_dim)])
	for i in range(y_dim):
		m[i].append(-1)
		for j in range(12):
			m[i] += (5 * [level[j + i * 12][-1]])
		m[i].append(-1)
	for i in range(24 - y_dim):
		m.append([0 if x not in [0, 61] else -1 for x in range(62)])
	m.insert(0, [-1 for _ in range(62)])
	return m


def choose_level(current_level):
	levels_init = [
		level_1_init, level_2_init, level_3_init, level_4_init, level_5_init, level_6_init,
		level_7_init, level_8_init, level_9_init, level_10_init,
	]
	y_dim, matrix, level, prizes_level, lift = levels_init[current_level-1]()
	return y_dim, matrix, level, prizes_level, lift


if __name__ == '__main__':
	choose_level(current_level)
