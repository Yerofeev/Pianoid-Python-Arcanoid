# coding: utf-8
import random
# ------------------------------------------------------ CONSTANTS ----------------------------------------------------#
BLANK = ' '
stop = 0
boss_levels = [10]
RESET_SETTINGS = '\033[0m'
colors = [
			'\033[91m', '\033[93m', '\033[32m',       # [red, yellow, green
			'\033[34m', '\033[37m', '\033[35m',       # blue , white, purple
			'\033[96m', '\033[33m', '\033[92m',       # light bl, or, light cyan
			'\033[05m', '\033[95m', '\033[5m',
			'\033[36m', '\033[40m', '\033[94m',
		]
symbols = ['🎵', '🎜', '♫', '🎶', '♩', '♬', '♯', '♭', '♮', '𝄢', '𝆔', '𝄪', '𝄫']
italic = '\33[3m'
bold = '\033[1m'
LIFT = colors[0] + bold + '🎚'
UNDERLINE = '\033[4m'
DISABLE = '\033[02m'
REVERSE = '\033[07m'

# ------------------------------------------------------ PRIZES CLASS--------------------------------------------------#
SURPRISE = colors[random.randint(0, 8)] + bold + ' 🎁 '
EXTEND = colors[8] + bold + '🡸 🡺 '
SHRINK = colors[0] + bold + '🡺 🡸 '
NEW_BALL = colors[8] + bold + '⏺' + RESET_SETTINGS + colors[6] + '🎵'
GLUE = colors[7] + bold + '𝄐𝄑 '
PROTECTION = [colors[7] + '🎧 ', colors[7] + bold + '🎧 ']
FASTER = colors[0] + bold + '𝆒  '
SLOWER = colors[8] + bold + '𝆓  '
DEATH_1 = colors[0] + bold + '🔕 '
DEATH_2 = colors[0] + bold + '🔇 '
EXTRA_LIFE = colors[4] + '🎹 '
BARLINE = bold + colors[2] + '𝄂𝄂'
AUTOPILOT = colors[9] + bold + '🖭 '
FIRE = colors[6] + bold + ' 𝆄 '
# ------------------------------------------------------ MONSTER CLASS-------------------------------------------------#
MONSTER_1 = colors[8] + bold + '🐍 '
MONSTER_2 = colors[6] + bold + '🤐 '
HINDRANCE_1 = RESET_SETTINGS + colors[11] + bold + '🌩 '
HINDRANCE_2 = colors[3] + bold + '🌪 '
EXPLOSION = [
	colors[1] + bold + '💥 ',
	colors[0] + bold + '💥 ',
	colors[0] + bold + '🟒 ',
	colors[0] + bold + '💥 '
	]
monsters = [MONSTER_1, MONSTER_2, HINDRANCE_1, HINDRANCE_2]
BOMBS = [
	colors[0] + bold + '🔕 ',
	colors[0] + bold + '🔇 ',
	colors[0] + bold + '💣  ',
	colors[6] + bold + '🗲 ',
	colors[1] + '🔥 ',
	colors[0] + bold + ' 𝆄 ',
	]
# ------------------------------------------------------ BALL CLASS----------------------------------------------------#
BALL = colors[1] + '⏺'

# ------------------------------------------------------ FONTS --------------------------------------------------------#
monsters_font = colors[0] + italic + ' Monsters'
hindrances_font = colors[0] + italic + ' Hindrances'
surprise_font = RESET_SETTINGS + colors[10] + italic + '   Musical Box'
extend_font = RESET_SETTINGS + colors[10] + italic + ' Octave++ '
shrink_font = RESET_SETTINGS + colors[10] + italic + ' Octave--'
new_ball_font = RESET_SETTINGS + colors[10] + italic + '   Polyphony'
glue_font = RESET_SETTINGS + colors[10] + italic + '  Fermata'

extra_life_font = RESET_SETTINGS + colors[10] + italic + '   Grand Piano'
faster_font = RESET_SETTINGS + colors[10] + italic + '  Crescendo'
slower_font = RESET_SETTINGS + colors[10] + italic + '  Diminuendo'
protection_font = RESET_SETTINGS + colors[10] + italic + '   Acoustic'
barline_font = RESET_SETTINGS + colors[10] + italic + '   Barlines'
autopilot_font = RESET_SETTINGS + colors[10] + italic + '   Kissin mode'
fire_font = RESET_SETTINGS + colors[10] + italic + '  Trills'
fire_instr = colors[0] + bold + 'Space' + RESET_SETTINGS + colors[8] + italic + ' Start&Fire'
pause_font = colors[0] + bold + 'P,p' + RESET_SETTINGS + colors[8] + italic + ' Pause'
quit_font = colors[0] + bold + 'Q' + RESET_SETTINGS + colors[8] + italic + ' Quit'
exit_font = colors[0] + bold + 'Esc' + RESET_SETTINGS + colors[8] + italic + '    Restart'
level_font = RESET_SETTINGS + italic + bold + colors[1] + '  Level #'
pause_message = colors[13] + bold + 'PAUSE'
BASS_CLEF = colors[2] + UNDERLINE + '𝄢'
MUSICAL_STAFF = colors[2] + UNDERLINE + '🎼'
REPRISE_LEFT = colors[2] + '𝄇 '
REPRISE_RIGHT = colors[2] + '𝄆 '
DASH = colors[8] + bold + '-'
# ------------------------------------------------------ PADDLE CLASS -------------------------------------------------#
TRILL = colors[6] + bold + '𝆃'
LIVES = colors[0] + bold + '𝄞 '
PIANO = '🎹'
PIANO_FIRE = bold + '𝆖' + RESET_SETTINGS
glue_color = colors[1] + '𝆮' + RESET_SETTINGS
paddle_font = colors[4]
AUTO_ = '𝄞'
barline = colors[2] + '𝄗'
# ------------------------------------------------------ BOSS CLASS ---------------------------------------------------#
BOSS = 0
BOSS_ = REVERSE
BOSS_FIRE = colors[6] + bold + '🗲 '
BOSS_LIVES = colors[0] + bold + '🎵'

# ------------------------------------------------------ SPECIAL MESSAGES----------------------------------------------#

game_over_font = colors[0] + bold + '🎵'
GAME_OVER = colors[1] + bold + 'GAME OVER'
COMPLETE_VICTORY = colors[0] + bold + '🎜 You have completed all levels!!! 🎝 '
ENTER_TO_MENU = colors[0] + bold + 'Press any key to exit'
NEW_LEVEL = colors[0] + bold + '🎜 You have won. Prepare for the next level! 🎝 '


# ----------------------------------------------------------Bricks------------------------------------------------------#
b0 = ['', 0]
b1 = [colors[0] + '🎵'*5, 1]
b1_0 = [colors[10] + '🎵'*5, 1]
b2 = [colors[10] + '🎜'*5, colors[10] + bold + '🎜'*5, 2]
b2_0 = [colors[1] + '🎜'*5, colors[1] + bold + '🎜'*5, 2]
b2_01 = [colors[1] + bold + '🎜'*5, 1]
b3 = [colors[8] + bold + '🎶'*5, 1]
b4 = [colors[7] + '🎵'*5, colors[0] + '🎵'*5, 2]
b5 = [colors[1] + bold + '♩'*5, 1]
b6 = [colors[7] + '♬'*5, colors[1] + bold + '♬'*5, 2]
b7 = [colors[12] + '♪'*5, colors[12] + bold + '♪'*5, 2]
b7_ = [colors[12] + bold + '♪'*5, 1]
b8 = [colors[3] + bold + '🎜'*5, colors[3] + '🎜'*5, 2]
b9 = [colors[2] + '🎵'*5, colors[2] + bold + '🎵'*5, 2]
b10 = [colors[9]+bold + '♩'*5, 1]
b11 = [colors[7] + '🎶'*5, colors[7] + bold + '🎶'*5, 2]
b12 = [colors[10] + bold + '♬'*5, colors[5] + '♬'*5, 2]
b13 = [colors[6] + '𝄢'*5, colors[6] + bold + '🏮' * 5, 2]
b14 = ['𝄞'*5, bold + '𝄞'*5, 2]
b15 = ['𝆑'*5, italic + '𝆑'*5, bold + '𝆑' * 5, 3]
b16 = [colors[7] + '𝆏'*5, colors[7] + italic + '𝆏'*5, colors[7] + bold + '𝆏'*5, 3]
# indestructible
b100 = [DISABLE + bold + '𝄛'*5, -1]
b100_0 = [colors[12] + bold + '𝄛'*5, -1]
b101 = [colors[4] + '🏯'*5, -1]
b102 = [colors[4] + '🏰'*5, -1]
# blinking
b110 = [colors[5] + '𝄜'*5, 'B', 1]  # blinking bricks
b111 = [colors[12] + '⌛'*5, 'B', 1]  # blinking bricks
b112 = [colors[4] + '⌛'*5, 'B', 1]  # blinking bricks
b113 = [colors[1] + '⌛'*5, 'B', 1]  # blinking bricks
# ------------------------------------------------------MENU--------------------------------------------------#
CLEF = colors[0] + bold + '𝄞'
NEW_GAME = colors[8] + bold + italic + ' New  Game'
CHOOSE_LEVEL = colors[8] + bold + italic + 'Levels'
HELP = colors[8] + bold + italic + 'Help'
QUIT = colors[8] + bold + italic + 'Quit'
RETURN_MENT = colors[8] + bold + italic + 'Return to menu'
level_font_menu = colors[8] + bold + italic + 'Level'
red_note = colors[0] + bold + '🎵'
slim_note = colors[12] + '♪'
yellow_note = colors[1] + bold + '🎵'
green_note = colors[8] + bold + '🎵'
bottom_note = colors[14] + '🎵'
BREND = colors[6] + bold + italic + 'PIANOID'
PRIZES_HELP = colors[0] + italic + 'P r i z e s  t y p e s : '
TIPS = colors[0] + italic + 'T i p s  a n d  t r i c k s :'
