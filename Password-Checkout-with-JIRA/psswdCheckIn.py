# Copyright 2016 Centrify Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import json
from jira.client import JIRA
import cgi
import ConfigParser
import sys

# This Python script connects to Centrify 's Identity Service through REST API
# To check back in a privilege account password
# password is rotated before check - in

#reading variables from config file
config = ConfigParser.ConfigParser()
config.read('config.ini')

# Variables
_rowKey = ''
checkout_COID = sys.argv[1]
issueID = sys.argv[2]

jira_user = config.get('Properties', 'jira_user')
jira_password = config.get('Properties', 'jira_password')
jira_server = config.get('Properties', 'jira_url')
jira_project_key = config.get('Properties', 'jira_project')

# Connect to Cloud Service Tenant
tenant = config.get('Properties', 'c_tenant')
tpsswd = config.get('Properties', 'tpsswd')
c_user = config.get('Properties', 'c_user')

print '****************************************************************'
print ' '
print 'Connecting to Cloud Service...'
print ' '
print '****************************************************************'
print ' '
print('Tenant ID: ' + tenant)
print ' '
print '****************************************************************'

url = 'https://%s/security/login/' % tenant
payload = {
  'user': c_user,
  'password': tpsswd
}

verify = True
#Authentication to the Cloud Service
response = requests.get(url, params = payload, verify = verify)# print('response URL: ' + response.url)

response.raise_for_status()
auth = response.json()['Result']['Auth']

cookie = response.cookies['.ASPXAUTH']# print 'Cookie is %s' % response.cookies['.ASPXAUTH']

#Example of checking back in a password for a privilege account
print ' '
url = 'https://%s/ServerManage/CheckinPassword' % tenant
headers = {
  'X-CENTRIFY-NATIVE-CLIENT': '1',
  'Authorization': 'Bearer %s' % cookie,
  'Content-Type': 'application/json'
}
print 'Initiating password check-in for Check-OUT ID: ' + checkout_COID
r = requests.post(url, json = {
  "ID": checkout_COID
}, headers = headers, verify = verify)
r.raise_for_status
responseObject = r.json()
print 'Password CheckIn Execution: '
print 'Value:'
print responseObject['Result']
print 'Checked-IN: OK'
print ' '
print '****************************************************************'
print ' '

url = 'https://%s/ServerManage/RotatePassword' % tenant
headers = {
  'X-CENTRIFY-NATIVE-CLIENT': '1',
  'Authorization': 'Bearer %s' % cookie,
  'Content-Type': 'application/json'
}
r = requests.post(url, json = {
  "ID": _rowKey
}, headers = headers, verify = verify)
r.raise_for_status
responseObject = r.json()
print 'Rotating Password after Check-In: '
print ' '

print 'Closing JIRA Ticket'

options = {
  'server': jira_server
}

jira = JIRA(options, basic_auth = (jira_user, jira_password))

issue = jira.issue(issueID)
transitions = jira.transitions(issue)
print ' '
#print[(t['id'], t['name']) for t in transitions]# print[(t['id'], t['name']) for t in transitions]
comment = jira.add_comment(issueID, 'Password Checked In & Rotated - Closing Issue')
jira.transition_issue(issue, '31')
# EOF
