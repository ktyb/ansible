#!/usr/bin/python

from ansible.module_utils.basic import *
import requests


api_url = "https://graph.microsoft.com/v1.0/users/"

def gen_pass():
	value = "Kdw23#odkr45"

	return value

def patch_change_password(pb_data, new_pass):
	user_id = pb_data["user_id"]
	url = api_url + user_id

	token = pb_data["token"]

	headers = {
		'Content-Type': 'application/json',
		'Authorization': 'Bearer ' + token
	}
	
	payload = "{\r\n  \"passwordProfile\": {\r\n    \"password\": \"%s\",\r\n    \"forceChangePasswordNextSignIn\": false\r\n  }\r\n}" %new_pass
	response = requests.request("PATCH", url, headers=headers, data = payload)
	
	if response.status_code == 204:
		return True, str(response)
	
	return False, str(response)

def main():

	fields = {
		"token": {"required": True, "type": "str"},
		"user_id": {"required": True, "type": "str"}
	}

	module = AnsibleModule(argument_spec=fields)
	new_pass = gen_pass()			#getting new password from untroubled site
	status, response = patch_change_password(module.params, new_pass)
	

	module.exit_json(changed=status, meta=dict(passy=new_pass, result=response))
	

if __name__ == '__main__':
    main()
