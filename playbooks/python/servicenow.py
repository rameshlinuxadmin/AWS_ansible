import requests
import json
from requests.auth import HTTPBasicAuth

with open('/mnt/e/AWS_ansible/playbooks/python/data.json', 'r') as file:
    data = json.load(file)

print("service now instance is", data['instance'])

# ServiceNow instance info
instance = data['instance']
username = data['username']
password = data['password']
sys_id = data['group']
#istate = "2"

url = f"https://{instance}/api/now/table/incident"

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

conditions = [
	f'assignment_group.sys_id={sys_id}',
#	f'state={istate}'
]
query_params = {
	"sysparm_query": '^'.join(conditions)
}

response = requests.get(url, auth=HTTPBasicAuth(username, password),  params=query_params, headers=headers)
 
tmp = response.json()
#inc = tmp['result'][0]['number']

for i in tmp['result']:
  print(i['number'])

'''
if response.status_code == 200:
   incidents = response.json().get('result', [])
   for incident in incidents:
       incident_sys_id = incident['sys_id']
       patch_url = f"{url}/{incident_sys_id}"

       payload = {
         "state": "3",
      	 "work_notes": "Auto moved incident to new state to ignore the SLA breach"
       }

       patch_response = requests.patch(patch_url, auth=HTTPBasicAuth(username, password), headers=headers, json=payload)

       if patch_response.status_code == 200:
         print(f"Updated incident {incident_sys_id}")
       else:
         print(f"Failed to update incident {incident_sys_id}: {patch_response.status_code}")
else:
    print(f"Failed to retrieve incidents: {response.status_code} - {response.text}")
'''
