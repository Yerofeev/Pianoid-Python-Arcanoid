import os
import platform
import sys
import tty
import termios
import threading
import time
import sys
import select
import pygame, curses
from time import sleep
from random import randint

colors = ['\033[91m', '\033[93m', '\033[32m', '\033[34m', '\033[37m', '\033[35m', '\033[96m']  #[red,yellow,green,blue,white,purple,light blue] #Extented ANSI
M = [[1 for x in range(63)] for y in range(18)]
color_level_1 = [[i%2] if (i//12)%2==0 else [(i-1)%2] for i in range(84)]
prizes_level_1 = [0 if x not in [76,77,80] else 1 for x in range(84)]
prizes_level_1[75] = 1; prizes_level_1[80] = 2; prizes_level_1[81] = 3

prizes = {}
balls = {}

def print_there(x,y,text):   
   sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y, x, text))
   sys.stdout.flush()
   return

def getChar():
    fd = sys.stdin.fileno()
    oldSettings = termios.tcgetattr(fd)
    while True:
        try:
            tty.setcbreak(fd)
            answer = sys.stdin.read(1)
            if answer == '\x1b':          #'\x1b[D' Left_Arrow     splitting into two parts!!!
                answer = sys.stdin.read(2)   #https://stackoverflow.com/questions/7310958/is-it-possible-to-use-getch-to-obtain-inputs-of-varying-length
                if answer == '[D':
                    return answer
                if answer == '[C':
                    return answer
                else:
                    continue
            if answer == '1':
                return answer
            if answer == '2':
                return answer   
            if answer == '3':
                return answer
            if answer == '4':
                return answer
            if answer == 'q':
                 sys.exit()
            else:  break
        finally:
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)
    return answer	

def preliminaries():
    os.system('clear')
    os.system('setterm -cursor off') 
    print_there(0,0,'\033[32m'+chr(9608)*62+'\033[0m')
    for i in range(1,21):
        print_there(0,i+1,'\033[32m'+chr(9608)+ ' '*60 + chr(9608) + '\033[0m')


class Prize():

    def __init__(self, i ,x ,y, paddle,bricks):
        prizes_types = ['⟺', '⏺', '⏹']  #    9830'♥'   🕯 '🚀'   '⟺'    '❤ '
        self.prize_type = prizes_types[i-1]
        self.prize_x = x
        self.prize_y = y
        self.threading = threading.Thread(target=self.prize, args=(self.prize_type,self.prize_x,self.prize_y, paddle,bricks))
        self.threading.daemon = True
        return

    def prize_daemon(self):
        self.threading.start()

    def prize(self,prize_type,x,y,paddle,bricks):
            while y != 21:
                print_there(x+1,y,self.prize_type)
                sleep(0.1)
                print_there(x+1,y,' '*1)
                y += 1
            if self.prize_type == '⏹':
                paddle.length -= 2
                paddle.paint()
            elif self.prize_type == '⟺':   # chr(10231)
                paddle.length += 2
                paddle.paint()
            elif self.prize_type == '⏺':
                while True:
                    i = 1
                    if i not in balls:
                        balls[i] = Ball(x+1, y-1, 0.1)
                        balls[i].ball_deamon(bricks, paddle)
                        break
                    i += 1

class Bricks():
    
    def __init__(self,i):
        #Bricks.obj_x = [x for x in range(2,62) if x not in range(7,62,6)]
        #Bricks.obj_y = [y for y in range(1,9)]
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
            if self.prize != 0:

                prizes[i] = Prize(self.prize, x, y-1, paddle, bricks)
                prizes[i].prize_daemon()
                self.prize = 0
            return
        print_there((i%12)*5+2, i//12 + 2, self.color + chr(9608) + chr(9608)*3 + chr(9608))

        
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
        print_there(0, 22, ' '*80)                   #SORT OUT  LATER!!!
        for i in range(self.length): 
            print_there(self.position+i, 22, '\033[32m' + chr(10735) )                 #chr(8718) ∎  #chr(10735)⧯       chr(9209) '⏹'
        print_there(  70, 22, '\033[91m' + '❤ '*self.lives) #FINISH LATER!!! 
        

class Ball:

    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        Ball.speed = speed
        
    def ball_deamon(self, bricks, paddle):
        self.threading = threading.Thread(target=self.ball_display, args=(self.x, self.y, bricks,paddle))
        self.threading.daemon = True
        self.threading.start()       
    
    def ball_set_speed(speed):
        Ball.speed = speed

    def ball_display(self,x,y, bricks, paddle):
        i, j = 1, -1
        q = 0
        while True:             #while x != 0 and y != 0 and x != 62 and y != 22:
            x += i
            y += j  # position of the ball in the next moment
            print_there(x, y,  '⏺')
            sleep(Ball.speed)
            print_there( x, y, '\033[93m' + ' ')        

            
            # Next moment  #---------------------------------------#-----------------------------#
            if y  <= 2:
                if (x ) >= 60:
                    i = -i
                j = -j
            if (x + i) <= 1 or (x + i) >= 59:
                if (y + j) <= 1:
                    j = -j
                i = -i
            if (y ) >= 21:
                j = - j  # delete!!!!!
            if 2 < y < 10:
                #print('x', x, 'y', y, end='')
                try:
                    if M[y-1][x] != 0:
                        if y <= 8 and M[(y)][x + i] != 0:        # if obj in x-nearby
                            obj_num = (y - 2) * 12 + (x-2+i) // 5            # butt of the brick
                            #print('x', x, 'y', y,'objx', obj_num,' ', end='')
                            bricks[obj_num].paint_bricks(paddle, bricks, x=(((x-2+i)//5)*5)+2, y=y+1, i=obj_num,mode=1)    #y+1 on our line
                            sleep(Ball.speed/2)
                            i = -i
                        obj_num = (y - 3)*12 + (x-2)//5
                        #print('x', x, 'y', y,'objy',obj_num,' ',end='')
                        bricks[obj_num].paint_bricks(paddle, bricks, x=(((x-2)//5)*5)+2, y=y , i=obj_num,mode=1)
                        j = -j


                    elif M[y-1][x+i] != 0:                             # diag case
                        obj_num = (y - 3) * 12 + (x-2+i) // 5
                        #print('i', i, 'x', x, 'y', y, 'objd', obj_num, M[y - 1][x + i], ' ', end='')
                        bricks[obj_num].paint_bricks(paddle,bricks, x=(((x - 2+i) // 5) * 5) + 2, y=y,i=obj_num, mode=1)
                        if (x-2)%5 == 4 or (x-2)%5 == 1:                        #if in last pixel  -
                           # print('i',i,'x', x, 'y', y, 'objd', obj_num,M[y-2][x+i], ' ', end='')
                            if M[y-2][x+i] != 0:                                       # but if there is brick in next moment then no
                                i = -i
                            else: j = -j
                        else:
                            i = -i
                except IndexError:
                    print('x', x, 'y', y, 'Eobj', obj_num, ' ', end='')



            
def main():
   # start_time = time.time()
    preliminaries()
   # print("--- %s seconds ---" % (time.time() - start_time))
    paddle = Paddle(10, 3, 10)              #create paddle
    paddle.paint()                      #draw paddle
    bricks = [Bricks(i) for i in range(84)]          #create bricks
    for i in range(84):
        bricks[i].paint_bricks(paddle, bricks, i=i,mode=0)                  #draw bricks   # sort out paddle
    balls[0] = Ball(12, 15, 0.1)  # Create ball (x,y,speed)
    balls[0].ball_deamon(bricks, paddle)            #balls_thread
    while paddle.lives > 0:
        while len(Bricks.d) != 3:
            event = getChar()
            if event == '[D':
                direction = 'left'
                paddle.move(direction)
                paddle.paint()
            elif event == '[C':
                direction = 'right'    
                paddle.move(direction)
                paddle.paint()       
            elif event == '1':
                Ball.ball_set_speed(1)
            elif event == '2':
                Ball.ball_set_speed(0.2)
            elif event == '3':
                Ball.ball_set_speed(0.02)
            elif event == '4':
                Ball.ball_set_speed(0.005)
        print('OK')
        sleep(1)
        sys.exit()


if __name__=='__main__':
    try:
        
        main()
    finally:
        print('\033[0m')   
        os.system('setterm -cursor on')
        os.system('clear')



