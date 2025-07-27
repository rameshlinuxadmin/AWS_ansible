import requests
from requests.auth import HTTPBasicAuth

# ServiceNow instance info
instance = "dev330868.service-now.com"
username = "admin"
password = "/ju+In1RpYU8"
queue_sys_id = "cfcbad03d711110050f5edcb9e61038f"  # Replace with your queue sys_id

# API endpoints
base_url = f"https://{instance}/api/now/table/incident"

# Query parameters to fetch incidents in 'New' state assigned to your queue
query_params = {
    'sysparm_query': f'state=2^assignment_group={queue_sys_id}',
    'sysparm_fields': 'sys_id,number,state',
    'sysparm_limit': '100'
}

auth = HTTPBasicAuth(username, password)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Step 1: Get list of incidents in New state assigned to queue
response = requests.get(base_url, headers=headers, auth=auth, params=query_params)
response.raise_for_status()
data = response.json()

incidents = data.get('result', [])
if not incidents:
    print("No incidents in 'New' state found in the queue.")
    exit()

print(f"Found {len(incidents)} incidents in 'In progress' state to update.")

# Step 2: Loop and update each incident to 'In Progress' (state=2)
for incident in incidents:
    sys_id = incident['sys_id']
    number = incident['number']
    update_url = f"{base_url}/{sys_id}"

    payload = {
        "state": "3",
        "work_notes": "State changed to On Hold by Python script"
    }

    update_response = requests.patch(update_url, headers=headers, auth=auth, json=payload)
    if update_response.status_code == 200:
        print(f"Updated incident {number} to 'In Progress'.")
    else:
        print(f"Failed to update incident {number}: {update_response.status_code} {update_response.text}")

