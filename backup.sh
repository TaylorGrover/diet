#! /bin/bash

## This script simply copies all the relevant stored data into a backup folder during debugging

! [ -d /data/data/com.termux/files/home/food_logs ] && mkdir /data/data/com.termux/files/home/food_logs
! [ -d /data/data/com.termux/files/home/backup_diet ] && mkdir /data/data/com.termus/files/home/backup_diet && exit

cp /data/data/com.termux/files/home/food_logs/* /data/data/com.termux/files/home/backup_diet/logs/
cp /data/data/com.termux/files/home/
