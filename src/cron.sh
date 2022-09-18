#!/bin/bash 
# this is a script to restart the bot every so often.
# This is intended to be run using crontab

killall "python3" # kills the current process
screen -X -S bot quit # kills the current screen
cd /home/$USER/bots/Kryptonite-Bot/ # changes to the right directory. only works if you use the same file structure
screen -dmS bot
screen -dm bash -c "python3 src/main.py" # executes the commands into the screen
