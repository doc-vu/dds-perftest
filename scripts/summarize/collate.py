import pandas as pd
import numpy as np

def collate_util(sizes,input_path,output_path,endpoint_type):
  with open('%s/util_%s.csv'%(output_path,endpoint_type),'w') as fd:
    fd.write('payload,cpu(avg),cpu(std),mem(avg),mem(std)\n') 
    for size in sizes:
      data=pd.read_csv('%s/%d/util/summary_%s.csv'%(input_path,size,endpoint_type),\
        names=['bbb','cpu','mem'],skiprows=1,delimiter=',')
      avg_cpu=np.mean(data['cpu'])
      std_cpu=np.std(data['cpu'])
      
      avg_mem=np.mean(data['mem'])
      std_mem=np.std(data['mem'])

      fd.write('%d,%f,%f,%f,%f\n'%(size,avg_cpu,std_cpu,avg_mem,std_mem))

def collate_throughput(sizes,input_path,output_path):
  with open('%s/throughput.csv'%(output_path),'w') as fd: 
    fd.write('payload,throughput(avg),throughput(std),los(avg),lost(std)\n')
    for size in sizes:
      data=pd.read_csv('%s/%d/summary_sub.csv'%(input_path,size),\
        names=['bbb','length','count','packets/s','mbps','lost(%)','cpu'],skiprows=1,delimiter=',')
      avg_throughput=np.mean(data['packets/s'])
      std_throughput=np.std(data['packets/s'])
      
      avg_lost=np.mean(data['lost(%)'])
      std_lost=np.std(data['lost(%)'])

      fd.write('%d,%f,%f,%f,%f\n'%(size,avg_throughput,std_throughput,avg_lost,std_lost))

def collate_latency(sizes,input_path,output_path):
  with open('%s/latency.csv'%(output_path),'w') as fd:
    fd.write('payload,latency(avg),latency(std),90th(us),90th(std)\n')
    for size in sizes:
      data=pd.read_csv('%s/%d/summary_pub.csv'%(input_path,size),\
        names=['bbb','length','avg','std','min','max','50%','90%','99%','99.99%','99.9999%','cpu'],\
        skiprows=1,delimiter=',')
      avg_latency_avg=np.mean(data['avg'])
      std_latency_avg=np.std(data['avg'])
      
      avg_latency_90th=np.mean(data['90%'])
      std_latency_90th=np.std(data['90%'])

      fd.write('%d,%f,%f,%f,%f\n'%(size,avg_latency_avg,std_latency_avg,avg_latency_90th,std_latency_90th))

if __name__=="__main__":
  collate_util([64*2**i for i in range(10)],\
    '/home/kharesp/workspace/ansible/bbb/logs/multisub/reliable',\
    '/home/kharesp/workspace/ansible/bbb/plots/data/multisub/reliable','sub')
  collate_util([64*2**i for i in range(10)],\
    '/home/kharesp/workspace/ansible/bbb/logs/multisub/best_effort',\
    '/home/kharesp/workspace/ansible/bbb/plots/data/multisub/best_effort','sub')

  collate_util([64*2**i for i in range(10)],\
    '/home/kharesp/workspace/ansible/bbb/logs/multisub/reliable',\
    '/home/kharesp/workspace/ansible/bbb/plots/data/multisub/reliable','pub')
  collate_util([64*2**i for i in range(10)],\
    '/home/kharesp/workspace/ansible/bbb/logs/multisub/best_effort',\
    '/home/kharesp/workspace/ansible/bbb/plots/data/multisub/best_effort','pub')
