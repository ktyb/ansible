#!/usr/bin/python

from ansible.module_utils.basic import *
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen


api_url = "https://graph.microsoft.com/v1.0/users/"
pass_url = "https://untroubled.org/pwgen/ppgen.cgi"	#can set some parameters to url for stronger password

def gen_pass():
	html_site = urlopen(pass_url).read()
	bs = BeautifulSoup(html_site, features="lxml")
	table = bs.findAll('table')[2]
	value = table.select('tt')[0].text

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
