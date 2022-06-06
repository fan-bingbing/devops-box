import subprocess
import json

raw = subprocess.run(["terraform", "output", "-json"], capture_output=True).stdout

ips = raw.decode('utf-8')
resp_dict = json.loads(ips)
ip1=resp_dict['ip1']['value']
ip2=resp_dict['ip2']['value']

with open('./ansible/hosts', 'r') as file:
    # read a list of lines into data
    data = file.readlines()

# now change lines, note that you have to add a newline
data[9] = 'target2 ansible_host=' + ip1 + '\n'
data[15] = 'target3 ansible_host=' + ip2 + '\n'

# and write everything back
with open('./ansible/hosts', 'w') as file:
    file.writelines( data )
