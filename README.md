Pianoid.
Pianoid is yet another arkanoid-game, implemented in Python2.7-3.x. The distinctive feature of this game is its musical theme: your paddle is a piano, almost all prizes are connected to the music world and decor is filled with musical flavor.

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

Downside of the game is that control is very rough, much time it's better to quickly click Left/ight instead of continuosly pressing it.

Screens:





![![alt text]](https://github.com/Yerofeev/Pianoid-Python-Arkanoid/blob/master/pics/Selection_002.png)
![![alt text]](https://github.com/Yerofeev/Pianoid-Python-Arkanoid/blob/master/pics/Selection_007.png)
![![alt text]](https://github.com/Yerofeev/Pianoid-Python-Arkanoid/blob/master/pics/Selection_004.png)
![![alt text]](https://github.com/Yerofeev/Pianoid-Python-Arkanoid/blob/master/pics/Selection_003.png)


How to Play:
1. git clone https://github.com/Yerofeev/Pianoid-Python-Arkanoid.git
2. cd Pianoid-Python-Arkanoid
3. python(3) pianoid.py
4. Enjoy!
