#!/bin/bash

start_time=`date +%s`


echo 'Hello'


end_time=`date +%s`
runtime=$((end_time-start_time))
mins=$((runtime / 60))
script=$(basename $BASH_SOURCE)

if [ $? -ne 0 ]; then
  echo "Your job (${script}) returned non-zero status (${mins} mins)." | slack_notifier
else
  echo "Your job (${script}) was successfully done (${mins} mins)." | slack_notifier
fi
