import os,argparse
import query_es
import pandas as pd
import numpy as np

def get_utilization_data(test_dir):
  files = (f for f in os.listdir(test_dir) 
           if os.path.isfile(os.path.join(test_dir, f)))
  
  #ensure util directory exists
  if not os.path.exists('%s/util'%(test_dir)):
    os.makedirs('%s/util'%(test_dir))
  
  for f in files:
    if f.startswith('sub') or f.startswith('pub'):
      print('processing file:%s'%(f))
      hostname=f.partition('_')[2].partition('.')[0]
      #get start and end ts
      with open('%s/ts/%s'%(test_dir,f),'r') as fd:
        start_ts,end_ts = fd.readline().rstrip().split(',')
      #get cpu and memory usage from es
      query_es.query(hostname,'perftest_cpp',int(start_ts),int(end_ts),'%s/util/%s'%(test_dir,f))

def average_utilization(path,endpoint_type):
  with open('%s/summary_%s.csv'%(path,endpoint_type),'w') as fd: 
    fd.write('bbb,avg_cpu,avg_mem\n')
    for file_name in os.listdir(path):
      if file_name.startswith(endpoint_type):
        data=pd.read_csv('%s/%s'%(path,file_name),\
          names=['cpu','mem'],skiprows=1,delimiter=',')
        bbb= file_name.partition('_')[2].partition('.')[0]
        avg_cpu= np.average(data['cpu'])
        avg_mem= np.average(data['mem'])
        fd.write('%s,%f,%f\n'%(bbb,avg_cpu,avg_mem))

if __name__=="__main__":
  parser=argparse.ArgumentParser(description='script to query elastic search to get utilization data for an experiment run')
  parser.add_argument('-log_dir',help='log directory path',required=True)
  args=parser.parse_args()

  for length in [64*2**i for i in range(10)]:
    print('Getting utilization data for size:%d\n'%(length))
    get_utilization_data('%s/%d'%(args.log_dir,length))
    average_utilization('%s/%d/util'%(args.log_dir,length),'pub')
    average_utilization('%s/%d/util'%(args.log_dir,length),'sub')
