#!/bin/bash
stdbuf -oL ./base_station.py $1 | gpsd -n -N -D 3 /dev/stdin