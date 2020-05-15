from PIL import ImageGrab
import time
import cv2
import sys
import re
import threading
from easy_ocr import ocr_image

import keyboard

import mouse

import numpy as np
start = 0
print("Input checkvalue:")
check_value =int(input())
print("Input move1 x:")
move1_x =int(input())
print("Input move1 y:")
move1_y =int(input())
print("Input move2 x:")
move2_x =int(input())
print("Input move2 y:")
move2_y =int(input())



def move():
    global value
    while 1:
           print(value)
           if value < check_value:
               print("move1")
               mouse.move(move1_x, move1_y, absolute=True, duration=0.25)
               mouse.click()
           elif value==99999:
               time.sleep(5)
           else:
               print("move2")
               mouse.move(move2_x, move2_y, absolute=True, duration=0.25)
               mouse.click()
               
           time.sleep(5)
 

def set_roi():
    global ROI_SET, x1, y1, x2, y2
    global start
    start = 1
    ROI_SET = False
    print("Select your ROI using mouse drag.")
    while(mouse.is_pressed() == False):

        x1, y1 = mouse.get_position()

        while(mouse.is_pressed() == True):

            x2, y2 = mouse.get_position()

            while(mouse.is_pressed() == False):

                print("Your ROI : {0}, {1}, {2}, {3}".format(x1, y1, x2, y2))

                ROI_SET = True
                return x1,y1,x2,y2


    
def stop():
   sys.exit(0)
 


ROI_SET = False

x1,y1,x2,y2 = set_roi()

global value
value =20
th1 = threading.Thread(target=move)
while True:
    if start == 1:
       th1.start()
       start = 2
    if ROI_SET == True:
        image = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(x1, y1, x2, y2))), cv2.COLOR_BGR2RGB)
        cv2.imwrite('image.png',image)
        try:
            value1=ocr_image('image.png',service='qq')
            value2 = re.findall("\d+",value1[0])
            value = float(value2[0])
        except:
            value = 99999


        cv2.imshow("image", image)

        key = cv2.waitKey(100)

        if key == ord("q"):

            print("Quit")

            break
 

cv2.destroyAllWindows()
