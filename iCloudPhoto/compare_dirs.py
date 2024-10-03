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

# Note: This version expect the left list file
#
import os

# Directory where you want to search for the files
directory = '/mnt/c/temp'
# List of filenames to search for
left_filename = 'rphotosum.txt'
right_filename = "dphotos.txt"

# Path to where the left files reside
left_path = '/mnt/r/iCloud Photos/Photos'

print('Read lists of file names and check whether for each filename on the')
print('left, whether it can be found in the right side as well.')
print()

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
    right_lines = [line.rstrip().split('/') for line in fh.readlines()]
print ('Right file no of lines: ',len(right_lines))
right_fns =[]
for line in right_lines:
    right_fns.append(line[1])
#print (right_fns)

print("Files not found on the right side:")
for fn in left_fns:
    try:
        idx = right_fns.index(fn)
        #print(idx, right_lines[idx])
    except ValueError:
#        print ("*** File <"+fn+"> not found in right file.")
        print (os.path.join(left_path, fn))

print("That#s all folks...")
