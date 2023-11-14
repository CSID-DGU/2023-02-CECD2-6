#!/bin/bash

new_cron_job="* * * * * /bin/bash -c 'source \$HOME/.bashrc; python3 \$GDSPATH/NewsData/newsdata.py >> \$GDSPATH/ShellLogs/runNewsdata.log 2>&1'"
(crontab -l; echo "$new_cron_job") | crontab -
