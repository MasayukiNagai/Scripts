#!/bin/bash

# quit existing screens (presumably from the previous runs)
screen -ls  | egrep "^\s*[0-9]+.run_job*" | awk -F "." '{print $1}' | xargs -I {} screen -S {} -X quit

# start new screens
num_screens=5
for ((i=0; i<num_screens; i++)); do
  screen -mdS run_job$i  # opens detached screens
done

# throw jobs to screens
num_jobs=10
iscreen=0
for ((job_id=0; job_id<num_jobs; job_id++)); do
  screen -S run_job${iscreen} -X stuff \
  "python test.py ${iscreen} ${job_id}^M"
  ((iscreen=iscreen+1))
  if (( iscreen >= num_screens ))
  then
    iscreen=0
  fi
done
