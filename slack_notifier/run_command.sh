#!/bin/bash

COMMAND=$1

HOST=`hostname`
DATE=`date`
start=`date +%s`

$COMMAND

if [ $? -ne 0 ]; then
  job_msg="Your job returned non-zero status."
else
  job_msg="Your job was successfully done."
fi

end=`date +%s`
runtime=$((end-start))
min=$((run_time / 60))
sec=$((run_time % 60))

msg="CMD: ${COMMAND}\n"
msg+="DATE: ${DATE}\n"
msg+="HOST: ${HOST}\n"
msg+="Run time: ${min} (min) ${sec} (sec)\n"
msg+="Comment: $job_msg"

echo -e ${msg} | slack_webhook.sh
