#!/bin/bash
eval "export $(egrep -z DBUS_SESSION_BUS_ADDRESS /proc/$(pgrep -u $LOGNAME gnome-session)/environ | tr '\0' '\n')"
python3 ~/pc_status/pc_status.py $1 $2 $3 $4 $5 $6 $7 $8
