import os
import platform
import sys
import tty
import termios
import threading
import time
import sys
from time import sleep
from random import randint

def getChar():
    """Dynamically reads one symbol entered by player,
    then either add one symbol to the code
    or perform comparison to the secret code or exits"""
    fd = sys.stdin.fileno()
    oldSettings = termios.tcgetattr(fd)
    while True:
        try:
            tty.setcbreak(fd)
            answer = sys.stdin.read(3)
            if answer == '\x1b[D':
                    sys.exit()
            else:  continue
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)
    return answer	

class Paddle:

    def __init__(self, length, lives):
        self.length = length
        self.lives = lives
        

class Ball:

    def __init__(self,x,y,speed):
        self.x = x
        self.y = y
        self.speed = speed
        
        
    def ball_display(x,y,speed):  
        i, j = 1, -1
        while True:
            while x != 0 and y != 0 and x != 70 and y != 22:
                print_there(y, x, '\033[93m' + '⏺')
                sleep(speed)
                print_there(y, x, '\033[93m' + ' ')        
                x += i
                y += j   
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
                
    def ball_deamon(self):
        self.threading = threading.Thread(target=ball_display, args=(self.x,self.y,self.speed))
        self.threading.daemon = True
        self.threading.start()                    
  



def print_there(x,y,text):   
    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
    sys.stdout.flush()
    return

def main():
    os.system('clear')
    os.system('setterm -cursor off')  
    ball1 = Ball(5, 65, 0.1)
    ball1.ball_deamon()
    while True:
            print_there(20, 70, '\033[91m' + '❤ '*3)
            event = getChar()
            

if __name__=='__main__':
    try:
        main()
    finally:
        print('\033[0m')   
        os.system('setterm -cursor on')
        os.system('clear')



