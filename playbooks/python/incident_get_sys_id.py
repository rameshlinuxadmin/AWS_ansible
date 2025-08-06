import requests
from requests.auth import HTTPBasicAuth
import json

with open('/mnt/e/AWS_ansible/playbooks/python/data.json', 'r') as file:
    data = json.load(file)

print("service now instance is", data['instance'])

instance = data['instance']
username = data['username']
password = data['password']
group_name = "Team Development Code Reviewers"

url = f"https://{instance}/api/now/table/sys_user_group"
query_params = {
    'sysparm_query': f'name={group_name}',
    'sysparm_fields': 'sys_id,name',
    'sysparm_limit': '1'
}

auth = HTTPBasicAuth(username, password)
headers = {
    "Accept": "application/json"
}

response = requests.get(url, headers=headers, auth=auth, params=query_params)
response.raise_for_status()
data = response.json()

groups = data.get('result', [])
if groups:
    group = groups[0]
    print(f"Group found: {group['name']} with sys_id: {group['sys_id']}")
else:
    print(f"No group found with name '{group_name}'.")
