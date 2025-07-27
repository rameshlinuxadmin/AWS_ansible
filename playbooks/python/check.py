import json
import requests 
from requests.auth import HTTPBasicAuth

with open('/mnt/e/AWS_ansible/playbooks/python/data.json', 'r') as file:
    data = json.load(file)

print("service now instance is", data['instance'])

instance = data['instance']
username = data['username']
password = data['password']
#assignment_group_name = data['group']
#state = "*"

url = f"https://{instance}/api/now/table/incident"

#conditions = [
#	f'assignment_group={assignment_group_name}',
#	f'state={state}'
#]

query_params = {
	#'sysparm_query': '^'.join(conditions),
	'sysparm_query': f'state=1',
	'sysparm_limit': '5'
}

auth = HTTPBasicAuth(username, password)
headers = {
    "Accept": "application/json"
}

response = requests.get(url, headers=headers, auth=auth, params=query_params)
#response.raise_for_status()
tmpout = response.json()
for i in tmpout['result']:
	state_code = i['state']
	if state_code == '2':
		print(i['number'], 'is In-progress')
	elif state_code == '3':
                print(i['number'], 'is On Hold')
	else:
                print(i['number'], 'is New')

