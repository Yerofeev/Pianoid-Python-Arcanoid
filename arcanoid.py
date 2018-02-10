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

def print_there(x,y,text):   
    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y, x, text))
    sys.stdout.flush()
    return


def getChar():
    """Dynamically reads one symbol entered by player"""
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
            if answer == 'q':
                print('Quit')
                sleep(0.2)
                sys.exit()                       
            else:  break
        finally:
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)
    return answer	

def bricks(level_file):
    for j in range(4):    
        for i in range(11):
                print_there (  2+i*6, 1+j*2,  '\033[96m' + chr(9604)*5 + ' ')
                print_there (  2+i*6, 2+j*2,  '\033[96m' + chr(9608)*5 + ' ')        #chr(9608)'█'
    objects_x = [x for x in range(70) if (x-1)%6 != 0]                                  #Why here?????????????????
    objects_y = [y+1 for y in range(8)]
    return objects_x, objects_y            

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
            print_there(self.position+i, 22, '\033[32m' + chr(10735) )                 #chr(8718) ∎  #chr(10735)⧯       chr(9209) ' ⏹'
        print_there(  70, 22, '\033[91m' + '❤ '*self.lives) #FINISH LATER!!! 


class Ball:

    def __init__(self,x,y,speed):
        self.x = x
        self.y = y
        self.speed = speed
        
    def ball_deamon(self,objects_x, objects_y):
        self.threading = threading.Thread(target=self.ball_display, args=(self.x,self.y,self.speed,objects_x, objects_y))
        self.threading.daemon = True
        self.threading.start()       
        
    def ball_display(self,x,y,speed,objects_x, objects_y):  
        i, j = 1, -1
        while True:
            while x != 0 and y != 0 and x != 70 and y != 22:
                print_there(x, y, '\033[93m' + '⏺')
                sleep(0.1)
                print_there( x, y, '\033[93m' + ' ')        
                x += i
                y += j   
                #print(objects_y,y-1)
                if y-1 in objects_y:
                    num_obj = x//6
                    print_there (2+num_obj*6, y-1,  ' '*6)        
                    print_there (2+num_obj*6, y-2,  ' '*6)        #chr(9608)'█'   
                    j=1
                    x+=1
            if y == 0 and x == 70:
                i = -1
                j = 1
                x = 69
                y = 1
            if x == 0:
                i = 1
                x = 2
                y += 1
            elif y == 0:
                j = 1
                x +=1
                y = 2
            elif x == 70:
                i = -1
                x = 69
                y -= 1
            elif y == 22:
                j = -1
                x +=1
                y = 20
  




def main():
    os.system('clear')
    os.system('setterm -cursor off')  
    ball_1 = Ball(22, 12, 0.1)
    paddle = Paddle(10, 3, 10)
    objects_x, objects_y      = bricks(1)
    paddle.paint()
    ball_1.ball_deamon(objects_x, objects_y)
    while True:
            event = getChar()
            if event == '[D':
                direction = 'left'
                paddle.move(direction)
                paddle.paint()
            elif event == '[C':
                direction = 'right'
                paddle.move(direction)
                paddle.paint()                
   
            

if __name__=='__main__':
    try:
        main()
    finally:
        print('\033[0m')   
        os.system('setterm -cursor on')
        os.system('clear')



