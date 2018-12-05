#!/bin/bash

if [ $# -ne 3 ]; then
  echo 'usage:' $0 'command identifier log_dir' 
  exit 1
fi

command_str=$1
identifier=$2
log_dir=$3

#change into perftest dir
cd /home/riaps/dev_environ/dds/perftest


#get start ts
start_ts=`date +%s`

#execute perftest
$command_str 2>$log_dir/err/$identifier.csv 1>$log_dir/$identifier.csv

#get end ts
end_ts=`date +%s`

#log start & end ts
echo $start_ts,$end_ts > $log_dir/ts/$identifier.csv

#log command used for execution of perftest
echo $command_str > $log_dir/cmd/$identifier.csv
