import subprocess,os,argparse,time
import numpy as np

if __name__=="__main__":
  parser=argparse.ArgumentParser(description='script to start latency test for different payload sizes')
  parser.add_argument('-numSubscribers',help='number of subscribers',type=int,required=True)
  parser.add_argument('-output_dir',help='output directory under which test results will be logged',required=True)
  parser.add_argument('-bestEffort',help='flag for bestEffort QoS use. Default is reliable QoS.',action='store_true')

  args=parser.parse_args()

  #payload sizes
  #data_lengths=[64*2**i for i in range(0,10)]
  data_lengths=[256]

  #ensure output_dir exists
  if not  os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)

  for idx,length in enumerate(data_lengths):
    print('\n\n\nStarting test:%d for dataLen:%d'%(idx,length))
  
    #ensure directory exists
    log_dir='%s/%d'%(args.output_dir,length)
    if not  os.path.exists(log_dir):
      os.makedirs(log_dir)
  
    #start subscribers
    if args.bestEffort:
      subprocess.check_call(['ansible-playbook','playbooks/experiment/subscriber.yml',\
        '--limit','all[0:%d]'%(args.numSubscribers-1),"--extra-vars=detachedMode=True multiSubTest=True keyed=True extra_params=' -bestEffort'"])
    else:
      subprocess.check_call(['ansible-playbook','playbooks/experiment/subscriber.yml',\
        '--limit','all[0:%d]'%(args.numSubscribers-1),'--extra-vars=detachedMode=True multiSubTest=True keyed=True'])
  
    #start publisher
    if args.bestEffort:
      subprocess.check_call(['ansible-playbook','playbooks/experiment/publisher.yml',\
        '--limit','all[%d]'%(args.numSubscribers), "--extra-vars=executionTime=300 numSubscribers=%d dataLen=%d latencyTest=True keyed=True extra_params=' -bestEffort'"%(args.numSubscribers,length)])
    else:
      subprocess.check_call(['ansible-playbook','playbooks/experiment/publisher.yml',\
        '--limit','all[%d]'%(args.numSubscribers), '--extra-vars=executionTime=300 numSubscribers=%d dataLen=%d latencyTest=True keyed=True'%(args.numSubscribers,length)])
  
    #wait for some time before collecting logs
    time.sleep(5)

    #collect logs
    subprocess.check_call(['ansible-playbook','playbooks/util/copy.yml',\
      '--limit','all[0:%d]'%(args.numSubscribers),'--extra-vars=src_dir=/home/riaps/log/  dest_dir=%s'%(log_dir)])
