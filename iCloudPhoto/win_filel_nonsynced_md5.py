# This program iterates through a cloud sync directory and writes
# the MD5 hashes together with the filename  to an output text file.
#
# An example is to calculate the file hases of an iCloud Photo directory.
#
# Cloud sync directory means that file entries be already be downloaded
# from the cloud (synced) or just point to the cloud (non-synced).
# When accessing a non-synced file the OS downloads the file under cover
# before opening it.
# In order to only create MD5 hashes of files already downloaded, it
# determines the file's size on the disk.
# It can be used to checks whether files in an iCloud Photo directory
# are synced or not. For a non-synced file the size on disk is 0.
#
# The output file contains an entry for each file where the hash for
# a non-synced file is a number of zeros.
#
# We could not find out how to determine which on disk space a file occupies
# under WinLinux. So wie took an Windows specific approach using the
# ctypes module.
# Therefore his progarm must in a windows shell.
#


import os
import ctypes
import hashlib

if os.name != 'nt':
    print("*** Program must run under Windows ***")
    print("Aborting...")
    exit()

dir = "D:\\iCloudPhotos-Werner\\Photos"
##fns = ['4fedc65d-8c91-4f31-a8ec-daba787c1465.jpg', '6a2abca4-0f05-4f2b-a507-91f98886107d.jpg']

dir_out = ""
fn_out  = "photosum-d.txt"

# dir_lst = "C:\\temp"
# fn_lst  = "dphotos.txt"
'''
with open(os.path.join(dir_lst, fn_lst), "r") as fh:
    lines = [line.rstrip().split('/') for line in fh.readlines()]
print ('List file no of lines: ',len(lines))
fns =[]
for line in lines:
    fns.append(line[1])
#print (right_fns)
'''

filesizehigh=ctypes.c_ulonglong(0)
no_fnotsynced = 0
no_fmd5sum    = 0

print("Writing md5 hashes of synced files in directory <"+dir+"> to file ",os.path.join(dir_out,fn_out))
print("#",end="")

with open(os.path.join(dir_out,fn_out), 'w') as fout:

    #for fn in fns:
    #for fn in fns[0:10]:

    directory = os.fsencode(dir)
    for file in os.listdir(directory):
        fn = os.fsdecode(file)

        path = os.path.join(dir,fn)
        res = ctypes.windll.kernel32.GetCompressedFileSizeW(ctypes.c_wchar_p(path),ctypes.pointer(filesizehigh))

        if res == -1:
            print("Not found   - File <"+path+">")
        elif res == 0:
#            print("Not synced  - File <"+path+">")
            line = "00000000000000000000000000000000"+"  "+fn
            no_fnotsynced += 1
            print("-",end="", flush=True)
        else:
#            print("File size:  - File <"+path+">    - ",res)
            md5 = hashlib.md5(open(path,'rb').read()).hexdigest()
            line = md5+"  "+fn
            no_fmd5sum += 1
            print(".",end="",flush=True)

        fout.write(f"{line}\n")

print()
print("Files md5 hashed:", no_fmd5sum)
print("Files not synced:", no_fnotsynced)
