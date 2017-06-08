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
import ConfigParser
import sys

# This Python script connects to Centrify 's Identity Service
# through REST API# To get a list of Privilege Accounts associated with a Resource

# reading variables from config file
config = ConfigParser.ConfigParser()
config.read('config.ini')

resourceID = sys.argv[1]

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

verify = True# Authentication to the Cloud Service
response = requests.get(url, params = payload, verify = verify)# print('response URL: ' + response.url)

response.raise_for_status()
auth = response.json()['Result']['Auth']

cookie = response.cookies['.ASPXAUTH']# print 'Cookie is %s' % response.cookies['.ASPXAUTH']

# Example of getting a list of Privilege Accounts for a Resource
# This only pulls one Account ID for a given Resource
# Iteration / Loop needed here for scaling so you can see all accounts for a Resource

print ' '
print 'Listing Privilege Accounts for Resource: ' + resourceID
print ' '
url = 'https://%s/ServerManage/GetAccountsForResource' % tenant
headers = {
  'X-CENTRIFY-NATIVE-CLIENT': '1',
  'Authorization': 'Bearer %s' % cookie,
  'Content-Type': 'application/json'
}

r = requests.post(url, json = {
  "Computer": resourceID
}, headers = headers, verify = verify)
r.raise_for_status
responseObject = r.json()# print responseObject

print 'Privilege Account _RowKey: ' + responseObject['Result'][0]['_RowKey']
print 'Privilege Account _RowKey: ' + responseObject['Result'][1]['_RowKey']
print 'Privilege Account _RowKey: ' + responseObject['Result'][2]['_RowKey']

print ' '

print '****************************************************************'

#EOF
