#!/usr/bin/python

from ansible.module_utils.basic import *
import requests

host_url = "https://login.microsoftonline.com/"

def request_for_token(pb_data):
	tenant_id = pb_data["tenant_id"]
	url = host_url + tenant_id + "/oauth2/v2.0/token"
	
	auth_code = "authorization_code"
	client_id = pb_data["client_id"]
	scope = "https://graph.microsoft.com/.default"
	code = pb_data["code"]
	client_secret = pb_data["client_secret"]

	header = {
		"Content-type": "application/x-www-form-urlencoded"
	}

	body = {
		"client_id" : client_id,
		"scope" : scope,
		"redirect_uri": "http://localhost",
		"code" : code,
		"grant_type" : auth_code,
		"client_secret" : client_secret
	}
	
	response = requests.post(url, data=body, headers=header)

	if response.status_code == 200:
		return True, response.json()['access_token']
	
	return False, response.json()['error_description']

def main():

	fields = {
		"tenant_id": {"required": True, "type": "str"},
		"client_id": {"required": True, "type": "str"},
		"client_secret": {"required": True, "type": "str" },
		"code": {"required": True, "type": "str" }
	}

	module = AnsibleModule(argument_spec=fields)
	status, response = request_for_token(module.params)

	module.exit_json(changed=status, ansible_facts=dict(token=response))

if __name__ == '__main__':
    main()
