#!/usr/bin/python

from ansible.module_utils.basic import *
import requests

api_url = "https://graph.microsoft.com/beta/applications"

def prepare_header(token):
	headers = {
		'Content-Type': 'application/json',
		'Authorization': 'Bearer ' + token
	}
	return headers

def retrieve_app_list(token):
	response = requests.request("GET", api_url, headers=prepare_header(token))
	#print(response.json()['value'])
	if response.status_code == 200:
		dict_id = [d['id'] for d in response.json()['value']]
		return True, dict_id
	return False, response

def delete_only_user_apps(params):
	status, response = retrieve_app_list(params["token"])
	if status:
		ctr = 0
		for i in response:
			temp_url = api_url + "/" + i + "/owners"
			res = requests.request("GET", temp_url, headers=prepare_header(params["token"]))
			for values in res.json()['value']:
				owner = values['id']
				if owner == params["user_id"]:
					temp_url = api_url + "/" + i
					requests.request("DELETE", temp_url, headers=prepare_header(params["token"]))	#deleting all AD apps assiign to account
					ctr = ctr + 1
		return True, ("Deleted " + str(ctr) + " AD apps.")
	return False, str(response) #cant retrieve app list

def main():

	fields = {
		"token": {"required": True, "type": "str"},
		"user_id": {"required": True, "type": "str"}
	}

	module = AnsibleModule(argument_spec=fields)
	status, response = delete_only_user_apps(module.params)
	

	module.exit_json(changed=status, meta=dict(how_much_deleted=response))
	
if __name__ == '__main__':
    main()
