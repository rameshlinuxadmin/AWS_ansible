import requests
from requests.auth import HTTPBasicAuth

# ServiceNow instance info
instance = "dev330868.service-now.com"
username = "admin"
password = "/ju+In1RpYU8"
sys_id = "a83820b58f723300e7e16c7827bdeed2"

url = f"https://{instance}/api/now/table/incident/{sys_id}"

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

payload = {
    "state": "2",
    "work_notes": "State changed to In Progress by Python script"
}

response = requests.patch(url, auth=HTTPBasicAuth(username, password), json=payload, headers=headers)

if response.status_code == 200:
    print("Incident updated successfully.")
else:
    print(f"Failed to update incident: {response.status_code} {response.text}")
