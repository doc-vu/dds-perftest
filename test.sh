#!/bin/bash

for i in `seq 1 1`;
  do
     python scripts/experiment/latency_test.py  -numSubscribers 1 -output_dir /home/kharesp/workspace/ansible/bbb/logs/latency_test/one_subscriber/real_time_priority/reliable/run$i
  done 

#for i in `seq 2 3`;
#  do
#     python scripts/experiment/latency_test.py  -numSubscribers 1 -output_dir /home/kharesp/workspace/ansible/bbb/logs/latency_test/one_subscriber/best_effort/run$i  -bestEffort
#  done 
