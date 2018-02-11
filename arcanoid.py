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
level_1  = []
q=[]
for j in range(1,10):
   for  i in range(1,60,5):
      q.append(i)
      q.append(j)
      q.append((i+j)%2)
      level_1.append(q[-3:]) 
print(level_1)    
sleep(5)

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
         if answer == 's':
             return answer
         if answer == 'a':
             return answer   
         if answer == 'p':
             return answer                
         if answer == 'q':
             print('Quit')
             sleep(0.2)
             sys.exit()                 
         else:  break
      finally:
         termios.tcflush(sys.stdin, termios.TCIOFLUSH)
         termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)
   return answer	

def preliminaries():
    os.system('clear')
    os.system('setterm -cursor off') 
    print_there(0,0,'\033[32m'+chr(9608)*61+'\033[0m')
    for i in range(1,21):
        print_there(0,i+1,'\033[32m'+chr(9608)+ ' '*59 + chr(9608) + '\033[0m')
    
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
            print_there (2+i*6, 2+j*2,  '\033[96m' + ' '*6)
            print_there (2+i*6, 3+j*2,  '\033[96m' + ' '*6)        #chr(9608)'█'    

            #for k in range (2+i%10*6,i%10*6+6):
            #   Bricks.obj_x.remove(k)
            #Bricks.obj_y.remove((i//10+1)*2); Bricks.obj_y.remove((i//10+1)*2-1)            
            return
        j = i // 10
        i = i %  10
        if i % 2 == 0:
            print_there (2+i*5, 2+j*2, '\033[35m' + chr(9608) + chr(9608)*3 + chr(9608) )
            print_there (2+i*5, 3+j*2, '\033[91m' + chr(9608) + chr(9608)*3 + chr(9608) )        #chr(9608)'█'        
                                                  #is it possible to ?
        else:
            print_there (2+i*5, 2+j*2, '\033[93m' + chr(9608) + chr(9608)*3 + chr(9608) )
            print_there (2+i*5, 3+j*2, '\033[93m' + chr(9608) + chr(9608)*3 + chr(9608) )        #chr(9608)'█'                 
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
        self.threading = threading.Thread(target=self.ball_display, args=(self.x, self.y, bricks))
        self.threading.daemon = True
        self.threading.start()       
    
    def ball_set_speed(self, speed):
        self.speed = speed
    def ball_display(self,x,y, bricks):  
        i, j = 1, -1

        while True:             #while x != 0 and y != 0 and x != 62 and y != 22:
            
            print_there(x, y, '\033[93m' + '⏺')
            sleep(self.speed)
            print_there( x, y, '\033[93m' + ' ')        
            x += i; y += j                   #position of the ball in the next moment
            
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
                    if x in [x for x in range(1,62,6)] and y in [obj_num//10*2+1,obj_num//10*2+2]:
                        print('x',x)
                        j = -j
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
    preliminaries()
    ball_1 = Ball(23,23,1)#(56, 10, 0.1)                      
    paddle = Paddle(10, 3, 10)              #create paddle
    paddle.paint()                      #draw paddle
    bricks = [Bricks() for i in level_1]          #create bricks
    for i in len(level_1):
        bricks[i].paint_bricks(level_1[i],mode=0)                  #draw bricks                   
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
            elif event == 's':
                ball_1.ball_set_speed(3)
            elif event == 'a':
                ball_1.ball_set_speed(0.03)  
            elif event == 'p':
                ball_1.ball_set_speed(1)                   
   
            

if __name__=='__main__':
    try:
        print_there(1,1,chr(9608) + chr(9608)*3 + chr(9608))
        sleep(3)
        
        main()
    finally:
        print('\033[0m')   
        os.system('setterm -cursor on')
        os.system('clear')



