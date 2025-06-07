#!/usr/bin/python
#
# Python program to check if a directory is completely covered by another one.
# The check is performed based on to directory listings named left and right.
# The program checks for each filename in the file that the filename exits
# in the right file.
#
# Instead of adding complex argument line parsing and help functions, we define
# in the beginning of the code number of variables. They specify:
#  - directory where the left and right list files reside
#  - the filenames for the left and right list files
#  - the path to directory of the left files themselves, in order to
#    output a list of full pathnames of files that are missing on the right
#    side.
#
# 02.10.-2024 Werner Schollenberger

# Note: This version expects the left list file to contain the output of
#       a md5sum command on all files in the directory.
#       For right file (current iCloud dir) it is expected to contain
#       the parent directory (Photos) as part of the names,
#       e.g. "Photos/00d7ac61-cc99-46ac-ba3d-85fb303a37b9.jpg"
#

import os

if os.name == 'nt':
#    directory = 'C:\\temp'
    directory = ''
#    left_path = 'R:\\iCloud Photos\\Photos'
    left_path = 'R:\\iCloud Photos\\Downloads'

elif os.name == 'posix':
#    directory = '/mnt/c/temp'
    directory = ''
#    left_path = '/mnt/r/iCloud Photos/Photos'
    left_path = '/mnt/r/iCloud Photos/Downloads.old'
else:
    print("Unknown os type: ",os.name)
    print("Aborting...")
    exit()

# Directory where you want to search for the files
# List of filenames to search for
#left_filename = 'photosum-r.txt'
left_filename = 'photo_downloads-r.txt'

right_filename = "photosum-d.txt"
diff_filename ="photodown-diff.txt"

hash_nul = "00000000000000000000000000000000"
# Path to where the left files reside

print('Read lists of file names and check whether for each filename on the')
print('left, whether it can be found in the right side as well.')
print()
print("Write files that differ on both sides in file:   ",os.path.join(directory,diff_filename) )
print()
print('Left file: ',os.path.join(directory, left_filename),'    - Right file: ',os.path.join(directory, right_filename)  )

##'''
with open(os.path.join(directory, left_filename), "r") as fh:
    left_lines = [line.rstrip().split('  ') for line in fh.readlines()]
#print (left_lines)
print ('Left file no of lines:  ',len(left_lines))
left_fns =[]
for line in left_lines:
    left_fns.append(line[1])
#print(left_fns)
##'''
## For testing comment out block above and uncommend line below
## left_fns = ['00d7ac61-cc99-46ac-ba3d-85fb303a37b9.jpg', '0a620ef8-b07e-41c6-9b75-adee59677b02.jpg', 'not_in_there.jpg']

with open(os.path.join(directory, right_filename), "r") as fh:
    right_lines = [line.rstrip().split('  ') for line in fh.readlines()]
print ('Right file no of lines: ',len(right_lines))
right_fns =[]
for line in right_lines:
    right_fns.append(line[1])
#print (right_fns)

print()
print("Files not found on the right side (you may want to display them")
print ("using the batch command DisplayPhoto.bat in a Windows cmd window):")
print()
with open(os.path.join(directory,diff_filename), 'w') as fout:
    for hash, fn in left_lines:
#       for hash, fn in left_lines[0:100]:
        try:
            idx = right_fns.index(fn)
#           print(fn, hash, idx, right_lines[idx][0])
            if right_lines[idx][0] != hash_nul and hash != right_lines[idx][0]:
                fout.write(f"{fn}\n")
#                print("ooo Files differ for ", fn, "Hashes are: ",hash, right_lines[idx][0])
#            else:
#                print("+++ File ", fn, "is identical ")
        except ValueError:
#           print ("### File <"+fn+"> not found in right file.")
#            print (fn, end=" ")
            print (fn)
print()
print()
print("That's all folks...")
