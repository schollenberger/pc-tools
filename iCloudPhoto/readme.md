# iCloudPhoto Readme

Tools to check differences between the iCloud Photo directory and a backup of it.

## compare_dirs.py

Python program to check if a directory is completely covered by another one.
The check is performed based on to directory listings named left and right.
The program checks for each filename in the file that the filename exits
in the right file.

## win_check_disk_size.py

Must run under Windows !!

Checks whether a photo is synced or not by looking at the actual size on disk.
Takes file names from a list file.

## scratch_code.py

Code fragments that have been collected while browsing the internet.

## DisplayPhoto.bat

Call windows viewer via command line.

In order to inspect the photos from the backup that cannot be found in the
iCloud Photos directory, you can call the windows image viewer via command line
using this batch file.
It is based on the code sniplet below:
```
rundll32.exe "%ProgramFiles%\Windows Photo Viewer\PhotoViewer.dll", &<filename>
```
It is derived from: https://answers.microsoft.com/de-de/windows/forum/all/windows-fotoanzeige-%C3%BCber-die-commandline/e2a11c47-b961-41d5-9cf4-c9dcb33bb5bf

In the article the "ImageView_Fullscreen" parameter is present but it looks
like that it only opens the old Image Viewer window as well.
For completeness:
```
rundll32.exe "%ProgramFiles%\Windows Photo Viewer\PhotoViewer.dll", ImageView_Fullscreen &<filename>
```


## Todos and infos

### Todos:

 - generate list file with md5 checksup from iCloud Photos directory
   but only for the files that have been synced.
   Running 'md5sum' over this directory will cause all files to be
   downloaded.

 - Improve compare_dirs by verifiying md5 hases in the list files as
   well where possible.
