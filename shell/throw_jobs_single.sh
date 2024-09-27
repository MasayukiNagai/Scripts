#!/bin/bash

num_jobs=5
for ((job_id=0; job_id<num_jobs; job_id++)); do
  python test.py ${job_id}
done
