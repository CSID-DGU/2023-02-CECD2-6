#!/bin/bash

(crontab -l; echo "*/30 * * * * source $HOME/.bashrc; python3 $GDSPATH/NewsData/newsdata.py && echo \"\$(date +'\%Y-\%m-\%d \%H:\%M:\%S') - runNewsdata.sh executed successfully\" >> $GDSPATH/ShellLogs/runNewsdata.log || echo \"\$(date +'\%Y-\%m-\%d \%H:\%M:\%S') - runNewsdata.sh failed\" >> $GDSPATH/ShellLogs/runNewsdata.log") | crontab -
#(crontab -l; echo "* * * * * /usr/bin/python3 /home/pkoi5088/2023-02-CECD2-6/NewsData/newsdata.py >> /home/pkoi5088/2023-02-CECD2-6/logfile.log 2>&1") | crontab -
#(crontab -l; echo "* * * * * source /home/pkoi5088/.bashrc; /usr/bin/python3 /home/pkoi5088/2023-02-CECD2-6/NewsData/newsdata.py >> /home/pkoi5088/2023-02-CECD2-6/logfile.log 2>&1") | crontab -
