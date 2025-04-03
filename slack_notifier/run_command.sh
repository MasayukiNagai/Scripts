#!/bin/bash

COMMAND="$@"

HOST=$(hostname)
DATE=$(date '+%Y-%m-%d %H:%M:%S %Z')
start=$(date +%s)

$COMMAND

if [ $? -ne 0 ]; then
  job_msg="Your job returned non-zero status."
else
  job_msg="Your job was successfully done."
fi

end=$(date +%s)
run_time=$((end-start))
min=$((run_time / 60))
sec=$((run_time % 60))

msg="CMD: ${COMMAND}\n"
msg+="DATE: ${DATE}\n"
msg+="HOST: ${HOST}\n"
msg+="Run time: ${min} (min) ${sec} (sec)\n"
msg+="Comment: $job_msg"

echo -e ${msg} | slack_webhook.sh
