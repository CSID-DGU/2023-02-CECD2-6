#!/bin/bash

(crontab -l; echo "*/30 * * * * source $HOME/.bashrc; python3 $GDSPATH/NewsData/newsdata.py >> $GDSPATH/ShellLogs/runNewsdata.log 2>&1") | crontab -
#(crontab -l; echo "28 * * * * source $HOME/.bashrc; python3 $GDSPATH/NewsData/testNewsGenerator.py >> $GDSPATH/ShellLogs/runNewsdata.log 2>&1") | crontab -
