#!/usr/bin/python
#
# Scratch code collected while trying ot display the files on the left side
# under WinLinux.

import time

# code to display image
#from matplotlib import pyplot as plt
#from matplotlib import image as mpimg
# plt.xlabel("X pixel scaling")
# plt.ylabel("Y pixels scaling")
# plt.title(fn)
# image = mpimg.imread(img_name)
# plt.imshow(image)
# plt.show()
# time.sleep(5)

import sys
import cv2
#img = cv2.imread("sheep.png", cv2.IMREAD_ANYCOLOR)

#while True:
#    cv2.imshow("Sheep", img)
#    cv2.waitKey(0)
#    sys.exit() # to exit from all the processes

#cv2.destroyAllWindows() # destroy all windows

'''
        print ("    Displaying file:  ", img_name)
        img = cv2.imread(img_name, cv2.IMREAD_ANYCOLOR)
        cv2.imshow(img_name, img)
        cv2.waitKey(0)
'''
        #while True:
        #    cv2.imshow("Sheep", img)
        #    cv2.waitKey(0)
        #    sys.exit() # to exit from all the processes

        #cv2.destroyAllWindows() # destroy all windows
sys.exit()
cv2.destroyAllWindows()


## code to iterate over Directory
import os

directory = os.fsencode(directory_in_str)

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".asm") or filename.endswith(".py"):
        # print(os.path.join(directory, filename))
        continue
    else:
        continue

# Or recursively, using pathlib:

from pathlib import Path

pathlist = Path(directory_in_str).glob('**/*.asm')
for path in pathlist:
    # because path is object not string
    path_in_str = str(path)
    # print(path_in_str)
