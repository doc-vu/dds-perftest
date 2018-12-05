import pandas as pd
import numpy as np

def collate_util(sizes,runs,input_path,output_path,endpoint_type):
  cpu={}
  mem={}
  with open('%s/util_%s.csv'%(output_path,endpoint_type),'w') as fd:
    fd.write('payload,cpu(avg),cpu(std),mem(avg),mem(std)\n') 
    for size in sizes:
      for runid in runs:
        data=pd.read_csv('%s/run%d/%d/util/summary_%s.csv'%(input_path,runid,size,endpoint_type),\
          names=['bbb','cpu','mem'],skiprows=1,delimiter=',')
        if size in cpu: 
          cpu[size].append(np.mean(data['cpu']))
        else:
          cpu[size]=[np.mean(data['cpu'])]
       
        if size in mem: 
          mem[size].append(np.mean(data['mem']))
        else:
          mem[size]=[np.mean(data['mem'])]
    for size in sizes:
      fd.write('%d,%f,%f,%f,%f\n'%(size,np.mean(cpu[size]),np.std(cpu[size]),\
        np.mean(mem[size]),np.std(mem[size])))

def collate_throughput(sizes,runs,input_path,output_path):
  throughput={}
  lost={}
  with open('%s/throughput.csv'%(output_path),'w') as fd:
    fd.write('payload,throughput(avg),throughput(std),lost(avg),lost(std)\n')
    for size in sizes:
      for runid in runs:
        data=pd.read_csv('%s/run%d/%d/summary_sub.csv'%(input_path,runid,size),\
          names=['bbb','length','count','packets/s','mbps','lost(%)','cpu'],skiprows=1,delimiter=',')
        if size in throughput: 
          throughput[size].append(np.mean(data['packets/s']))
        else:
          throughput[size]=[np.mean(data['packets/s'])]
       
        if size in lost: 
          lost[size].append(np.mean(data['lost(%)']))
        else:
          lost[size]=[np.mean(data['lost(%)'])]
    
    for size in sizes:
      fd.write('%d,%f,%f,%f,%f\n'%(size,np.mean(throughput[size]),np.std(throughput[size]),\
        np.mean(lost[size]),np.std(lost[size])))
 
def collate_latency(sizes,runs,input_path,output_path):
  latency_avg={}
  latency_90th={}
  with open('%s/latency.csv'%(output_path),'w') as fd:
    fd.write('payload,latency(avg),latency(std),90th(avg),90th(std)\n')
    for size in sizes:
      for runid in runs:
        data=pd.read_csv('%s/run%d/%d/summary_pub.csv'%(input_path,runid,size),\
          names=['bbb','length','avg','std','min','max','50%','90%','99%','99.99%','99.9999%','cpu'],\
          skiprows=1,delimiter=',')
        if size in latency_avg: 
          latency_avg[size].append(np.mean(data['avg']))
        else:
          latency_avg[size]=[np.mean(data['avg'])]
       
        if size in latency_90th: 
          latency_90th[size].append(np.mean(data['90%']))
        else:
          latency_90th[size]=[np.mean(data['90%'])]
    for size in sizes:
      fd.write('%d,%f,%f,%f,%f\n'%(size,np.mean(latency_avg[size]),np.std(latency_avg[size]),\
        np.mean(latency_90th[size]),np.std(latency_90th[size])))

def collate_perftest_cpu(sizes,runs,input_path,output_path,endpoint_type):
  if endpoint_type=='pub':
    header=['bbb','length','avg','std','min','max','50%','90%','99%','99.99%','99.9999%','cpu']
  if endpoint_type=='sub':
    header=['bbb','length','count','packets/s','mbps','lost(%)','cpu']

  cpu={}
  with open('%s/perftest_cpu_%s.csv'%(output_path,endpoint_type),'w') as fd:
    fd.write('payload,cpu(avg),cpu(std)\n')
    for size in sizes:
      for runid in runs:
        data=pd.read_csv('%s/run%d/%d/summary_%s.csv'%(input_path,runid,size,endpoint_type),\
          names=header,skiprows=1,delimiter=',')
        if size in cpu: 
          cpu[size].append(np.mean(data['cpu']))
        else:
          cpu[size]=[np.mean(data['cpu'])]
       
    for size in sizes:
      fd.write('%d,%f,%f\n'%(size,np.mean(cpu[size]),np.std(cpu[size])))

if __name__=="__main__":
  collate_latency([64*2**i for i in range(10)],[1,2,3],\
    '/home/kharesp/workspace/ansible/bbb/logs/latency_test/one_subscriber/real_time_priority/reliable',\
    '/home/kharesp/workspace/ansible/bbb/plots/data/latency_test/one_subscriber/real_time_priority/reliable')
  
  collate_perftest_cpu([64*2**i for i in range(10)],[1,2,3],\
    '/home/kharesp/workspace/ansible/bbb/logs/latency_test/one_subscriber/real_time_priority/reliable',\
    '/home/kharesp/workspace/ansible/bbb/plots/data/latency_test/one_subscriber/real_time_priority/reliable',\
    'sub')

  collate_perftest_cpu([64*2**i for i in range(10)],[1,2,3],\
    '/home/kharesp/workspace/ansible/bbb/logs/latency_test/one_subscriber/real_time_priority/reliable',\
    '/home/kharesp/workspace/ansible/bbb/plots/data/latency_test/one_subscriber/real_time_priority/reliable',\
    'pub')
