Pianoid.
Pianoid is yet another arkanoid-game, implemented in Python. The distinctive feature of this game is its musical theme: your paddle is a piano, almost all prizes are connected to the music world and decor is filled with musical flavor.

Besides this pecularity the goal is the same as always in such games: crash all the bricks with the ball. Just to let you to contemplate the several seconds of the game process:


![![alt text]]( https://github.com/Yerofeev/Pianoid-Python-Arkanoid/blob/master/pics/pianoid_1.gif)

 As the second peculiar trait, PIANOID was written with NO use of PYgame, curses etc.. Only modules from standard library were used. The game is programmed for Linux terminals, the only dependencies are Python and support of extended ANSI.
Several general moments should be specified about some challenges and overall structure of the game:
1. Dynamical nonblocking input, processing both Arrows and Esc (details in engine.get_key())
2. Algorithm of ball's trajectory
3. Prizes, there are dozen of them. Much of the inspiration taken from Krypton Egg arkanoid-like game. 
The description of prizes can be found in help menu.
4. Boss level with its own logic and adversaries
5. Monsters appearing on all levels

How to install:
