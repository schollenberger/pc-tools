#

import os
import cv2
import numpy as np

if os.name == 'nt':
#    directory = 'C:\\temp'
    directory = ''
    left_path = 'R:\\iCloud Photos\\Photos'
    right_path = 'D:\\iCloudPhotos-Werner\\Photos'

elif os.name == 'posix':
#    directory = '/mnt/c/temp'
    directory = ''
    left_path = '/mnt/r/iCloud Photos/Photos'
    right_path = '/mnt/d/iCloudPhotos-Werner/Photos'
else:
    print("Unknown os type: ",os.name)
    print("Aborting...")
    exit()
diff_filename ="photosum-diff.txt"

with open(os.path.join(directory, diff_filename), "r") as fh:
    fnames = [line.rstrip() for line in fh.readlines()]

#print (left_lines)
print ('No of files to compare:  ',len(fnames))

#a = cv2.imread("sample-r.jpeg")
#b = cv2.imread("sample-d.jpeg")

for fn in fnames[0:100]:

    print()
    print("*** Comparing files  ",os.path.join(left_path, fn), "with ", os.path.join(right_path, fn))

    a = cv2.imread(os.path.join(left_path, fn))
    b = cv2.imread(os.path.join(right_path, fn))

#    print("Image 1: type and dimension size: ", type(a), a.ndim, a.size)
#    print("Image 1: color depth : ", a[0,0].size)
#    print("Image 1: X-dim       : ", a.size / a[0].size)
#    print("Image 1: Y-dim       : ", a[0].size / a[0,0].size)
#    print()
#    print("Image 2: type and dimension size: ", type(b), b.ndim, b.size)
#    print("Image 2: color depth : ", b[0,0].size)
#    print("Image 2: X-dim       : ", b.size / b[0].size)
#    print("Image 2: Y-dim       : ", b[0].size / b[0,0].size)

    diff = cv2.subtract(a, b)
#    print()
#    print("Diff-Img: type and dimension size: ", type(diff), diff.ndim, diff.size)
#    print("Diff-Img: color depth: ", diff[0,0].size)
#    print("Diff-Img: X-dim      : ", diff.size / diff[0].size)
#    print("Diff-Img: Y-dim      : ", diff[0].size / diff[0,0].size)


    max = 15
    arr2 = np.where(diff >= max)
#    no_pixels = 10000
#    while no_pixels >= 30:
#        arr2 = np.where(diff >= max)
#        no_pixels =  arr2[0].size
#        print("No of exceeding elements which differ more than ", max, ": ", arr2[0].size)
#        max += 1

#    print("Diff > ", max)
#    print(arr2)
    print("No of elements exceeding ", max, " : ", arr2[0].size)
#    for i in range(0,arr2[0].size):
#        print(arr2[0][i], arr2[1][i], arr2[2][i]," -> ", diff[arr2[0][i], arr2[1][i]] )


#    result = not np.any(diff)
    #print("Diff result:           ", result)
#    if result is True:
    if arr2[0].size < 20:
        print("*** Pictures are the nearly same")
    else:
        cv2.imwrite("diff-"+fn, diff)
        print("*** Pictures are different, the difference is stored as", "diff-"+fn)


print ("That's all...")
