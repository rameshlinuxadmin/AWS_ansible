import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta

with open('/mnt/e/AWS_ansible/playbooks/python/data.json', 'r') as file:
    data = json.load(file)

print("service now instance is", data['instance'])

# ServiceNow instance info
instance = data['instance']
username = data['username']
password = data['password']
sys_id = data['group']
istate = "3"

#URL for servicenow API
url = f"https://{instance}/api/now/table/incident"

#Headers for python execution
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

#Conditions
conditions = [
	f'assignment_group.sys_id={sys_id}',
	f'state={istate}'
]

#Querying the conditions mentioned above
query_params = {
	"sysparm_query": '^'.join(conditions)
}

#Fetching the values using the GET method based on the applied conditions
response = requests.get(url, auth=HTTPBasicAuth(username, password),  params=query_params, headers=headers)

#Storing the values temporarily to the variable
incidents = response.json().get('result', [])

# Helper function to calculate days since last update
def days_since_update(updated_on_str):
  last_updated = datetime.strptime(updated_on_str, "%Y-%m-%d %H:%M:%S")
  now = datetime.utcnow()
  delta = now - last_updated
  return delta.days

# Process each incident
for incident in incidents:
    number = incident['number']
    sys_id_inc = incident['sys_id']
    updated_on = incident['sys_updated_on'].split('.')[0].replace('T', ' ')
    days = days_since_update(updated_on)

    # Skip if updated within last 24 hrs
    #if days < 1:
    #    continue

    # Get work notes
    notes_url = f"https://{instance}/api/now/table/sys_journal_field"
    notes_query = {
        "sysparm_query": f"element_id={sys_id_inc}^element=work_notes",
        "sysparm_fields": "value,sys_created_on",
        "sysparm_limit": "10"
    }
    notes_resp = requests.get(notes_url, auth=HTTPBasicAuth(username, password), params=notes_query, headers=headers)
    notes = notes_resp.json().get('result', [])

    # Count existing strikes
    strike_count = sum(1 for n in notes if "STRIKE" in n['value'].upper())

    if strike_count < 1:
        note = f"STRIKE {strike_count + 1}: No update in 24 hours. Please provide update."
    elif strike_count == 1:
        note = "STRIKE 3: No update for 3 consecutive days. Ticket is being resolved."
    else:
        continue  # Already resolved or more than 3 strikes

    # Prepare update payload
    payload = {
        "work_notes": note
    }

    # Resolve on third strike
    if strike_count == 1:
        payload["state"] = "6"  # Resolved; replace with your actual resolved state code

    # Send update to incident
    update_url = f"https://{instance}/api/now/table/incident/{sys_id_inc}"
    update_resp = requests.patch(update_url, auth=HTTPBasicAuth(username, password), headers=headers, data=json.dumps(payload))

    print(f"Updated incident {number}")


