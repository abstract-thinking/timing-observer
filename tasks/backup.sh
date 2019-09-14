#!/bin/bash

# Get the archive date
archive_date="$(date +'%d-%b-%Y')"

# open database, wait up to 1 second for any activity to end and create a backup file
sqlite3 /home/markus/timing-observer/instance/rsl.sqlite << EOF
.timeout 1000
.backup /home/markus/timing-observer/backup/rsl_${archive_date}.sqlite3
EOF