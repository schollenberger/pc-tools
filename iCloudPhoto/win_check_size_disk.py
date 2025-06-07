# This program determines the file's size on the disk.
# It can be used to checks whether files in an iCloud Photo directory
# are synced or not. For a non-synced file the size on disk is 0.
#
# We could not find out how to determine which on disk space a file occupies
# under WinLinux. So wie took an Windows specific approach using the
# ctypes module.
# Therefore his progarm must in a windows shell.

# Note: This version expects the left list file to contain the output of
#       a md5sum command on all files in the directory.
#       For right file (current iCloud dir) it is expected to contain
#       the parent directory (Photos) as part of the names,
#       e.g. "Photos/00d7ac61-cc99-46ac-ba3d-85fb303a37b9.jpg"
#


import os
import ctypes

if os.name != 'nt':
    print("*** Program must run under Windows ***")
    print("Aborting...")
    exit()

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
