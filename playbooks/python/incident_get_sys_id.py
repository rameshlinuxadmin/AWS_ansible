import requests
from requests.auth import HTTPBasicAuth

instance = "dev330868.service-now.com"
username = "admin"
password = "/ju+In1RpYU8"
group_name = "Team Development Code Reviewers"  # Replace with your actual queue name

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
