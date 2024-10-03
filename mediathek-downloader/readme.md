# Mediathek-downloader Readme

The German TV stations ARD and ZDF make their Mediathek content available via
some Web interface (https://mediathekviewweb.de/).

## medathek-downloader.rb

Ruby program to batch download movies in different resolutions.  
Requires a control file. The template is media-file.txt.
To call the program easily copy the script run.sh to your media directory.

## exif_size.sh

Prints out the resolutions  of a list videos given as parameters.
It read the values from the EXIF section within the files.

It requires that you have the 'exiftool' installed.
See: https://exiftool.org/



