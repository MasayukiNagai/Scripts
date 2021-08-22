#!/bin/bash

COMMAND=$1

HOST=`hostname`
DATE=`date`
start=`date +%s`

$COMMAND

if [ $? -ne 0 ]; then
  msg="Your job returned non-zero status.\n"
else
  msg="Your job was successfully done.\n"
fi

end=`date +%s`
runtime=$((end-start))

msg+="CMD: ${COMMAND}\n"
msg+="DATE: ${DATE}\n"
msg+="HOST: ${HOST}\n"
msg+="Run time: ${runtime} (/s)"

echo -e ${msg} | slack_webhook.sh
