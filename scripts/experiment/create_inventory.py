import subprocess,re,os

#remove pre-existing inventory file 
#os.remove('inventory/nodes')

#run arp-scan command to get all connected devices on the network
output=subprocess.check_output(['sudo','arp-scan', '-I','eth0', '--localnet'])
#filter out lines that contain ip addresses   
regex=re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

#collect ip addresses
with open('inventory/ips','w') as f:
  for line in output.split('\n'):
    if re.match(regex, line):
      f.write(line.partition('\t')[0]+'\n')

#write inventory file
with open('inventory/ips','r') as f:
  for ip_addr in f:
    #execute ansible playbook to create inventory file
    subprocess.call(['ansible-playbook','playbooks/util/inventory.yml','--limit',ip_addr.strip()])

#remove file containing ips
os.remove('inventory/ips')
