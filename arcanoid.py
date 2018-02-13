import os
import platform
import tty
import termios
import threading
import sys
import select
import random
from time import sleep


colors = ['\033[91m', '\033[93m', '\033[32m', '\033[34m', '\033[37m', '\033[35m', '\033[96m']  #[red,yellow,green,blue,white,purple,light blue] #Extented ANSI
M = [[1 for x in range(63)] for y in range(18)]
color_level_1 = [[i%2] if (i//12)%2==0 else [(i-1)%2] for i in range(84)]
prizes_level_1 = [0 if x not in [76,77,80] else 0 for x in range(84)]
prizes_level_1[75] = 3; prizes_level_1[80] = 0; prizes_level_1[81] = 0
balls = {}
prizes = {}

def print_there(x,y,text):   
    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y, x, text))
    sys.stdout.flush()
    return

def isData():                          # https://stackoverflow.com/questions/2408560/python-nonblocking-console-input
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def preliminaries():
    os.system('clear')
    os.system('setterm -cursor off') 
    print_there(0,0,'\033[32m'+'\033[4m'+chr(9608)*62+'\033[0m')
    for i in range(1,21):
        print_there(0, i + 1, '\033[32m' + chr(9608) + ' '*60 + chr(9608) + '\033[0m')


class Prize:
    prizes_types = ['\033[92m' + '\033[1m' + '🡸 🡺 ', '\033[91m' + '\033[1m' + '🡺 🡸 ', ' ⏺ ']  # 9830'♥' 🏁 🌋 🕯 '🚀'   '⟺'    '❤ '
    def __init__(self, i ,x ,y, paddle,bricks):

        self.prize_type = Prize.prizes_types[i-1]
        self.prize_x = x
        self.prize_y = y
        self.threading = threading.Thread(target=self.prize, args=(self.prize_type,self.prize_x,self.prize_y, paddle,bricks))
        self.threading.daemon = True
        return

    def prize_daemon(self):
        self.threading.start()

    def prize(self,prize_type,x,y,paddle,bricks):
            while y != 21:
                print_there(x,y,self.prize_type)
                sleep(0.1)
                print_there(x,y,' '*4)
                y += 1
            if self.prize_type == Prize.prizes_types[0]:
                paddle.length += 2
                paddle.paint()
            elif self.prize_type == Prize.prizes_types[1]:   # chr(10231)
                paddle.length -= 2
                paddle.paint()
            elif self.prize_type == Prize.prizes_types[2]:
                while True:
                    i = 1
                    if i not in balls:
                        balls[i] = Ball(x+1, y-1)
                        balls[i].ball_deamon(bricks, paddle)
                    i += 1
                    break


class Bricks:
    
    def __init__(self,i):
        Bricks.d = {}
        self.status = 'ON'
        self.color = colors[color_level_1[i][0]]
        self.number = i
        self.prize = prizes_level_1[i]
    
    def paint_bricks(self, paddle, bricks, i=0, x=0, y=0, mode=0):
        if mode != 0:
            #print('(p)x',x,'y-1', y-1, ' ',end='')

            M[y-1][x:x+5] = [i-1 for i in M[y-1][x:x+5]]            #for k in range (2+i%10*6,i%10*6+6):
            if M[y-1][x] != 0: return
            self.status = 'OFF'
            Bricks.d[i]='OFF'
            print_there (x , y-1 , ' '*5)        #chr(9608)'█'
            #if self.prize != 0:
            #    prizes[i] = Prize(self.prize, x, y-1, paddle, bricks)
             #   prizes[i].prize_daemon()
            #    self.prize = 0
            return
        print_there((i % 12)*5 + 2, i//12 + 2, self.color + chr(9608) + chr(9608)*3 + chr(9608))

        
class Paddle:

    def __init__(self, length, lives, position):
        self.length = length
        self.lives = lives
        self.position = position
    
    def move(self, direction):
        if direction == 'left' and self.position >= 2:         
            self.position -= 2
        if direction == 'right' and self.length + self.position <= 60:
            self.position += 2                 
    
    def paint(self):
        print_there(0, 22, ' '*80)                   # SORT OUT  LATER!!!
        for i in range(self.length): 
            print_there(self.position+i, 22, '\033[32m' + '⧯')  # chr(8718) ∎  #chr(10735)⧯       chr(9209) '⏹'
        print_there(70, 22, '\033[91m' + '❤ '*self.lives)  # FINISH LATER!!!
        

class Ball:
    count = 0
    speed = 0.1

    def __init__(self, position, length):
        self.x = 19;position + length//2
        self.y = 10;21
        self.status = 'ON'
        Ball.count += 1
        print_there(self.x, self.y, '\033[96m' + '⏺')

    def paint_ball(self,position,length):
        print_there(self.x, self.y,  ' ')
        self.x = position + length//2
        print_there(self.x, self.y, '\033[96m' + '⏺')

        
    def ball_deamon(self, bricks, paddle):
        print_there(self.x, self.y,  ' ')
        self.threading = threading.Thread(target=self.ball_display, args=(self.x, self.y, bricks,paddle))
        self.threading.daemon = True
        self.threading.start()       
    
    def ball_set_speed(speed):
        Ball.speed = speed

    def ball_display(self,x,y, bricks, paddle):
        i = 1 #if random.random() < 0.5 else -1
        j = -1


        #q = 0

        while True:             #while x != 0 and y != 0 and x != 62 and y != 22:
            x += i
            y += j  # position of the ball in the next moment
            print_there(x, y, '\033[96m' + '⏺')
            sleep(Ball.speed)
            print_there( x, y, '\033[93m' + ' ')        

            
            # Next moment  #---------------------------------------#-----------------------------#
            if y  <= 2:
                if (x) >= 60:
                    i = -i
                j = -j

            if (x + i) <= 1 or (x + i) >= 60:
                if (y + j) <= 1:
                    j = -j
                i = -i
            if (y ) > 11:  #20
                j = -j; continue
                if x+1 == paddle.position or x-1 == paddle.position + paddle.length:  # -180* rebound from paddle's butt
                    i = -i
                    j = -j
                elif (x - paddle.position) > paddle.length or (x < paddle.position):
                    Ball.count -= 1
                    return
                else:
                    j = - j
            if 2 < y < 10:
                #print('x', x, 'y', y, end='')
                try:

                    #if j < 0:  # flying up
                        if M[y+j][x] != 0:
                            if y <= 8 and M[y][x + i] != 0:        # if obj in x-nearby
                                obj_num = (y - 3) * 12 + (x-2+i) // 5            # butt of the brick
                                print('x', x, 'y', y,'objyx', obj_num,' ', end='')
                                bricks[obj_num].paint_bricks(paddle, bricks, x=(((x-2+i)//5)*5)+2, y=y+j, i=obj_num,mode=1)    #y+1 on our line
                                sleep(Ball.speed/1.5)
                                i = -i
                            obj_num = (y + j - 2)*12 + (x-2)//5# (y - 3)*12 + (x-2)//5
                            print('x', x, 'y', y,'objy',obj_num,' ',end='')
                            bricks[obj_num].paint_bricks(paddle, bricks, x=(((x-2)//5)*5)+2, y=y , i=obj_num,mode=1)
                            j = -j
                            continue

                        elif   M[y][x+i] != 0: # x butt case
                            obj_num = (y - 3) * 12 + (x-2+i) // 5
                            print('i', i, 'x', x, 'y', y, 'objx', obj_num, M[y - 1][x + i], ' ', end='')
                            bricks[obj_num].paint_bricks(paddle, bricks, x=(((x - 2 + i) // 5) * 5) + 2, y=y+j, i=obj_num,  mode=1)
                            i = -i

                        elif M[y+j][x+i] != 0:                             # diag case
                            obj_num = (y - 3) * 12 + (x-2+i) // 5
                            print('i', i, 'x', x, 'y', y, 'objd', obj_num, M[y - 1][x + i], ' ', end='')
                            bricks[obj_num].paint_bricks(paddle,bricks, x=(((x - 2+i) // 5) * 5) + 2, y=y,i=obj_num, mode=1)
                            #if (x-2)%5 == 4 or (x-2)%5 == 1:                        #if in last pixel  -
                               # print('i',i,'x', x, 'y', y, 'objd', obj_num,M[y-2][x+i], ' ', end='')
                            #    if M[y-2][x+i] != 0:                  # but if there is brick in next moment then no
                            #        i = -i
                            #    else: j = -j
                            #else:
                             #   i = -i
                            i = -i; j = -j


                except IndexError:
                    print('x', x, 'y', y, 'Eobj', obj_num, ' ', end='')


def main():
    preliminaries()
    paddle = Paddle(10, 3, 25)  # create paddle
    paddle.paint()  # draw paddle
    bricks = [Bricks(i) for i in range(84)]  # create bricks
    for i in range(84):
        bricks[i].paint_bricks(paddle, bricks, i=i, mode=0)  # draw bricks   # sort out paddle

    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())
        while (len(Bricks.d)) < 84:
            while paddle.lives > 0:
                balls[0] = Ball(paddle.position, paddle.length)  # Create ball (x,y,speed)
                while Ball.count > 0:  # at least one ball isAlive
                    if isData():
                        answer = sys.stdin.read(1)
                        if answer == '\x1b':          #'\x1b[D' Left_Arrow     splitting into two parts!!!
                            answer = sys.stdin.read(2)   #https://stackoverflow.com/questions/7310958/is-it-possible-to-use-getch-to-obtain-inputs-of-varying-length
                            if answer == '[D':
                                direction = 'left'
                                paddle.move(direction)
                                if hasattr(balls[0], 'threading') is False:
                                    balls[0].paint_ball(paddle.position, paddle.length)
                                paddle.paint()
                            if answer == '[C':
                                direction = 'right'
                                paddle.move(direction)
                                if hasattr(balls[0], 'threading') is False:
                                    balls[0].paint_ball(paddle.position, paddle.length)
                                paddle.paint()
                            else:
                                continue
                        if answer == '1':
                            Ball.ball_set_speed(3)
                        if answer == '2':
                            Ball.ball_set_speed(0.1)
                        if answer == '3':
                            Ball.ball_set_speed(0.02)
                        if answer == '4':
                            Ball.ball_set_speed(0.005)
                        if answer == ' ':
                            balls[0].ball_deamon(bricks, paddle)  # balls_thread
                        if answer == 'q':
                             sys.exit()
                sleep(0.5)
                paddle.lives = paddle.lives - 1
                paddle.paint()
            print_there(25,14,'\033[91m'+'GAME OVER')
            sleep(2)
            sys.exit()




    finally:
          termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
          print('\033[0m')
          os.system('setterm -cursor on')
          os.system('clear')


if __name__=='__main__':
    main()




