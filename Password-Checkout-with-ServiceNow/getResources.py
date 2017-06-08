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
import pprint
import ConfigParser

# This is a basic script that uses Python to connect to Centrify's Identity Service
# through REST API
# This script retrieves a list of machine resources being managed by Privilege Manager

#reading variables from config file
config = ConfigParser.ConfigParser()
config.read('config.ini')

# Connect to Cloud Service Tenant
tenant = config.get('Properties','c_tenant')
tpsswd = config.get('Properties','tpsswd')
c_user = config.get('Properties','c_user')

print '****************************************************************'
print ' '
print 'Connecting to Cloud Service...'
print ' '
print '****************************************************************'
print ' '
print ('Tenant ID: ' + tenant)
print ' '
print '****************************************************************'
url = 'https://%s/security/login/' %tenant

payload = {'user': c_user, 'password': tpsswd}

verify = True
#Verify Authentication to the Cloud Service
response = requests.get(url, params=payload, verify=verify)
#print('response URL: '+ response.url)

#Retrieve cookie to use throughout session
cookie = response.cookies['.ASPXAUTH'] 
#print 'Cookie is %s' %response.cookies['.ASPXAUTH']  

headers = {'X-CENTRIFY-NATIVE-CLIENT': '1', 'Authorization': 'Bearer %s' %cookie, 'Content-Type': 'application/json'}

#Example of Getting a list of machine resources
#Example only pulls the first two resources

print ' '
print 'Print list of Privilege Service Resources: '
print ' '

url = 'https://%s/RedRock/query/' %tenant
r = requests.post(url, json={'Script': 'Select * from Server'},headers=headers,verify=verify)
r.raise_for_status
responseObject = r.json()

#Iteration/Loop should be implemented here for scaling

print 'ID: ' + responseObject['Result']['Results'][0]['Row']['ID'] + '	Type: ' + responseObject['Result']['Results'][0]['Row']['ComputerClass'] + '	Domain: ' + responseObject['Result']['Results'][0]['Row']['FQDN'] + '	State: ' + responseObject['Result']['Results'][0]['Row']['LastState']
print 'ID: ' + responseObject['Result']['Results'][1]['Row']['ID'] + '	Type: ' + responseObject['Result']['Results'][1]['Row']['ComputerClass'] + '	Domain: ' + responseObject['Result']['Results'][1]['Row']['FQDN'] + '	State: ' + responseObject['Result']['Results'][1]['Row']['LastState']

print ' '
print '****************************************************************'
print ' '
#EOF
