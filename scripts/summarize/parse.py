import os,argparse
pub_tags=['Length:','Latency:Ave','Std','Min','Max','50%','90%','99%','99.99%','99.9999%','CPU:']
sub_tags=['Length:','Packets:','Packets/s(ave):','Mbps(ave):','Lost:','CPU:']

def parse(endpoint_type,file_path):
  ascii_digits_dot=[46,48,49,50,51,52,53,54,55,56,57]
  if endpoint_type=='sub':
    tags=sub_tags
  elif endpoint_type=='pub':
    tags=pub_tags

  with open(file_path,'r') as f:
    while True:
      summary=f.next() 
      if summary.startswith('Length:'):
        break

  #remove all white spaces
  summary="".join(summary.split())

  results_dict={}

  for tag in tags:
    if tag=='Lost:':
      found_opening_parenthesis=False
      index=summary.find(tag)+len(tag)
      value=''
      for i in range(index,len(summary)-1):
        if (ord(summary[i])!=40 and not found_opening_parenthesis):
          continue
        if ord(summary[i])==40:
          found_opening_parenthesis=True
        if ord(summary[i])==37:
          break
        
        if (found_opening_parenthesis) and (ord(summary[i]) in ascii_digits_dot):
          value+=summary[i]

      results_dict[tag]=value
    else:
      index=summary.find(tag)+len(tag)
      value=''
      for i in range(index,len(summary)-1):
        if ord(summary[i]) in ascii_digits_dot:
          value+=summary[i]
        else:
          break
      results_dict[tag]=value
  
  return results_dict 

def summarize(endpoint_type,path):      
  files=os.listdir(path)
  with open('%s/summary_%s.csv'%(path,endpoint_type),'w') as of:
    if (endpoint_type=='pub'):
      of.write('bbb,length,avg,std,min,max,50%,90%,99%,99.99%,99.9999%,cpu\n')
      tags=pub_tags
    elif (endpoint_type=='sub'):
      of.write('bbb,length,count,packets/sec,mbps,lost(%),cpu\n')
      tags=sub_tags

    for fname in files:
      if fname.startswith(endpoint_type):
        bbb= fname.partition('_')[2].partition('.')[0]
        results= parse(endpoint_type,'%s/%s'%(path,fname))
        result_str='%s,'%(bbb)
        
        for tag in tags:
          result_str+=results[tag]+','
        of.write(result_str[:-1]+'\n')

if __name__=="__main__":
  parser=argparse.ArgumentParser(description='script to summarize publisher and subscriber side results for an experiment run')
  parser.add_argument('-log_dir',help='log directory path',required=True)
  args=parser.parse_args()
  for length in [64*2**i for i in range(10)]:
    summarize('pub','%s/%d'%(args.log_dir,length))
    summarize('sub','%s/%d'%(args.log_dir,length))
