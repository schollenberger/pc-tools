#!/bin/bash
#
# Call mediathek downloader program
#

# Be sure that the env. variable below is available, or  uncomment and adapt the line below.
#
# wsrepo_path = "/mnt/c/Users/.../pc-tools"     # path to git repo

ruby $wsrepo_path/pc-tools/mediathek-downloader/mediathek_downloader.rb $1
