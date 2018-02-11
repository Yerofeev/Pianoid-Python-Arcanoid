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

class Bricks():
    
    def __init__(self):
        Bricks.obj_x = [x for x in range(2,62) if x not in range(7,62,6)]
        Bricks.obj_y = [y for y in range(1,9)]  
        self.status = 'ON' 
    
    def paint_bricks(self, i, mode=0):
        if mode != 0:
            self.status = 'OFF'
            j = i // 10
            i = i %  10
            print_there (2+i*6, 1+j*2,  '\033[96m' + ' '*6)
            print_there (2+i*6, 2+j*2,  '\033[96m' + ' '*6)        #chr(9608)'█'    

            #for k in range (2+i%10*6,i%10*6+6):
            #   Bricks.obj_x.remove(k)
            #Bricks.obj_y.remove((i//10+1)*2); Bricks.obj_y.remove((i//10+1)*2-1)            
            return
        j = i // 10
        i = i %  10
        print_there (2+i*6, 1+j*2,  '\033[96m' + chr(9604)*5 + ' ')
        print_there (2+i*6, 2+j*2,  '\033[96m' + chr(9608)*5 + ' ')        #chr(9608)'█'        
        return                                      #is it possible to ?
    
    def delete_brick(self,x,y,i):

        print_there (-2+i%10*7, (i//10+1)*2-1,  ' '*6)
        print_there (-2+i%10*7, (i//10+1)*2,  ' '*6)        
        #print((i//10+1)*2,(i//10+1)*2-1)
        #sleep(30)
        return
        
        
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

    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        
    def ball_deamon(self, bricks):
        self.threading = threading.Thread(target=self.ball_display, args=(self.x, self.y, self.speed, bricks))
        self.threading.daemon = True
        self.threading.start()       
        
    def ball_display(self,x,y,speed, bricks):  
        i, j = 1, -1

        while True:             #while x != 0 and y != 0 and x != 62 and y != 22:
            
            print_there(x, y, '\033[93m' + '⏺')
            sleep(0.4)
            print_there( x, y, '\033[93m' + ' ')        
            x += i
            y += j
            
            # Next moment  #---------------------------------------#-----------------------------#
            if (y + j) <= 0:
                if (x + i) >= 60:
                    i = -i
                j = -j
            elif (y + j) in Bricks.obj_y and (x + i) in Bricks.obj_x:
                obj_num = int((y//2 - 1)*10 + (x // 6))
                #print('x',x,'y',y,obj_num,end='')
                if bricks[obj_num].status == 'ON':
                    bricks[obj_num].paint_bricks(obj_num,mode=1) 
                    if x in [x for x in range(1,62,6)]:
                        print('x',x)
                        i = -i
                    else:    
                        j = -j                        
                #sleep(30)
            elif (y + j) == 22:
                j =- j                      #delete!!!!! 
            elif (x + i) <= 0 or (x + i) >= 59:
                if (y + j) <= 0:
                    j = -j
                i = -i
                
            #elif (x + i) in Bricks.obj_x:
                
  




def main():
    os.system('clear')
    os.system('setterm -cursor off')  
    ball_1 = Ball(23,23,0.1)#(56, 10, 0.1)                      
    paddle = Paddle(10, 3, 10)              #create paddle
    paddle.paint()                      #draw paddle
    bricks = [Bricks() for i in range(40)]          #create bricks
    for i in range(40):
        bricks[i].paint_bricks(i,mode=0)                  #draw bricks                   
    ball_1.ball_deamon(bricks)            #balls_thread
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



