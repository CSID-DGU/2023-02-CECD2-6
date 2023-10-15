#!/bin/bash

(crontab -l; echo "* */1 * * * $GDSPATH/ShellFiles/runNewsdata.sh && echo \"\$(date +'\%Y-\%m-\%d \%H:\%M:\%S') - runNewsdata.sh executed successfully\" >> $GDSPATH/ShellLogs/runNewsdata.log || echo \"\$(date +'\%Y-\%m-\%d \%H:\%M:\%S') - runNewsdata.sh failed\" >> $GDSPATH/ShellLogs/runNewsdata.log") | crontab -
