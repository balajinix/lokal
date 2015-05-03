#! /usr/bin/env python

from facepy import GraphAPI
import sys

access_token = ''
try:
  with open('./access_token.txt') as f:
    lines = f.readlines()
    access_token = lines[0].strip()
except:
  print "Error geting access token"
  sys.exit()

graph = GraphAPI(access_token)
response = graph.get("/100004978365543/accounts")
if 'data' not in response:
  sys.exit()
print response
pages = response['data']
for page in pages:
  page_name = page['name']
  page_id = page['id']
  page_access_token = page['access_token']
  print page_name + '\t' + page_id + '\t' + page_access_token
