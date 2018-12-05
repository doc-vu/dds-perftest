import requests,datetime,argparse
from elasticsearch import Elasticsearch


def query(hostname,process_name,start_ts_s,end_ts_s,log_file):
  start_utc_ts=datetime.datetime.utcfromtimestamp(start_ts_s).strftime('%Y-%m-%dT%H:%M:%S')+'.000Z'
  end_utc_ts=datetime.datetime.utcfromtimestamp(end_ts_s).strftime('%Y-%m-%dT%H:%M:%S')+'.000Z'
  start_utc_date=datetime.datetime.utcfromtimestamp(start_ts_s).strftime('%Y.%m.%d')
  end_utc_date=datetime.datetime.utcfromtimestamp(end_ts_s).strftime('%Y.%m.%d')

  if (start_utc_date==end_utc_date):
    indices=['metricbeat-7.0.0-alpha1-%s'%(start_utc_date)]
  else:
    indices=['metricbeat-7.0.0-alpha1-%s'%(start_utc_date),'metricbeat-7.0.0-alpha1-%s'%(end_utc_date)]


  with open(log_file,'w') as fd: 
    fd.write('cpu(%),mem(%)\n')
    for index_name in indices:
      es = Elasticsearch([{'host': '172.21.20.29', 'port': 9200}])
      res= es.search(index=index_name,
        scroll='1m',
        size=1000,
        body={'query':{
                'bool': {
                  'must': [{'match': {'system.process.name':'perftest_cpp'}},
                           {'match': {'beat.hostname':'%s'%(hostname)}},
                          ],
                  'filter': {
                              'range':{
                                        '@timestamp':{
                                          'gte':'%s'%(start_utc_ts),
                                          'lte':'%s'%(end_utc_ts)
                                      }
                            }
                  }
                } 
             },
             'sort': [
                       {
                         '@timestamp': {
                           'order': 'asc'
                         }
                       }
                     ]
        })
      
      sid= res['_scroll_id']
      scroll_size = len(res['hits']['hits'])
      write(res,fd)
      
      while (scroll_size > 0):
        res = es.scroll(scroll_id = sid, scroll = '1m')
        # Update the scroll ID
        sid = res['_scroll_id']
        # Get the number of results that we returned in the last scroll
        scroll_size = len(res['hits']['hits'])
        # Do something with the obtained page
        write(res,fd)

  
def write(res,fd):
  for row in res['hits']['hits']:
    fd.write('%f,%f\n'%(float(row['_source']['system']['process']['cpu']['total']['pct'])*100,
      float(row['_source']['system']['process']['memory']['rss']['pct'])*100))


if __name__=="__main__":
  parser=argparse.ArgumentParser(description='script to get percentage cpu and memory use for a process from elasticsearch, given a range of timestamps and hostname')
  parser.add_argument('-start_ts',type=int,help='start ts in sec since epoch',required=True)
  parser.add_argument('-end_ts',type=int,help='end ts in sec since epoch',required=True)
  parser.add_argument('-hostname',help='hostname',required=True)
  parser.add_argument('-process_name',help='process name',required=True)
  parser.add_argument('-log_file',help='path of log file',required=True)
  args=parser.parse_args()
  query(args.hostname,args.process_name,args.start_ts,args.end_ts,args.log_file)
