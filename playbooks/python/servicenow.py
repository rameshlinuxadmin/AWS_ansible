import requests
from requests.auth import HTTPBasicAuth

# ServiceNow instance info
instance = "dev330868.service-now.com"
username = "admin"
password = "/ju+In1RpYU8"
#sys_id = "cfcbad03d711110050f5edcb9e61038f"
sys_id = "6816f79cc0a8016401c5a33be04be441"

url = f"https://{instance}/api/now/table/incident/sys_user/{sys_id}"

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

payload = {
    "state": "2",
    "work_notes": "State changed to In Progress by Python script"
}
'''
response = requests.patch(url, auth=HTTPBasicAuth(username, password), json=payload, headers=headers)

if response.status_code == 200:
    print("Incident updated successfully.")
else:
    print(f"Failed to update incident: {response.status_code} {response.text}")
'''

get_response = requests.get(url, auth=HTTPBasicAuth(username, password), headers=headers)
print(f"GET status: {get_response.status_code}")
print(get_response.text)
