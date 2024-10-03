#
# It is not easy to determine the space on disk a file occupies under WinLinux.
# This progarm must in a windows shell.

import os
import ctypes

dir = "D:\\iCloudPhotos-Werner\\Photos"
##fns = ['4fedc65d-8c91-4f31-a8ec-daba787c1465.jpg', '6a2abca4-0f05-4f2b-a507-91f98886107d.jpg']

dir_lst = "C:\\temp"
fn_lst  = "dphotos.txt"

with open(os.path.join(dir_lst, fn_lst), "r") as fh:
    lines = [line.rstrip().split('/') for line in fh.readlines()]
print ('List file no of lines: ',len(lines))
fns =[]
for line in lines:
    fns.append(line[1])
#print (right_fns)

filesizehigh=ctypes.c_ulonglong(0)

for fn in fns:
#for fn in fns[0:10]:
    path = os.path.join(dir,fn)
    res = ctypes.windll.kernel32.GetCompressedFileSizeW(ctypes.c_wchar_p(path),ctypes.pointer(filesizehigh))

    if res == -1:
        print("Not found   - File <"+path+">")
    elif res == 0:
        print("Not synced  - File <"+path+">")
    else:
        print("File size:  - File <"+path+">    - ",res)

print ("That's all folks ...")
