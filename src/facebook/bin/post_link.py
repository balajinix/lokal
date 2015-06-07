#! /usr/bin/env python

from facepy import GraphAPI
import sys
import urllib
import urllib2
import datetime
import time
from random import randint
from shutil import copyfile

debug = False
upload_history_file = "../logs/encroachment_revelation.txt"
log_file = "../logs/post_line.log"
#upload_link_url = 'http://loksattakarnataka.org/loksatta-revelation-details-of-encroachment-of-public-land-by-vips-and-their-relatives/'
upload_link_url = 'https://www.facebook.com/Loksattakarnataka/photos/a.197593726979656.48608.172917339447295/883413641730991/?type=1&permPage=1'

upload_hash = {}
def dump_file():
  timestamp = datetime.datetime.now().time().isoformat()
  new_file = log_file + "_" + timestamp
  f = open(new_file, 'w')
  for k, v in upload_hash.iteritems():
    f.write(k + '\t' + v + '\n')
  f.close()
  return new_file

access_token = ''
try:
  with open('../input/access_token.txt') as f:
    lines = f.readlines()
    access_token = lines[0].strip()
except:
  print "Error geting access token"
  sys.exit()

try:
  # we need to provide a file name to keep track of link ids
  with open(upload_history_file) as f:
    lines = f.readlines()
    for line in lines:
      line = line.strip()
      parts = line.split('\t')
      if len(parts) != 2:
        print "Error reading upload history file"
        print line
        continue
      page_id = parts[0]
      link_id = parts[1]
      if page_id not in upload_hash:
        upload_hash[page_id] = link_id
  f.close()
except:
  print "File not found: %s" % (upload_history_file)
      

graph = GraphAPI(access_token)
response = graph.get("/100004978365543/accounts")
pages = response['data']
count = 0
for page in pages:
  page_name = page['name']
  #if (page_name == 'Bengaluru LOKal'):
  #  continue
  page_id = page['id']
  if page_id in upload_hash:
    continue
  page_access_token = page['access_token']
  #print page_name + '\t' + page_id + '\t' + page_access_token
  if debug is True and page_name != 'LSPK Media Team':
      continue
  r = ''
  try:
    #print page_name + '\t' + page_id + '\t' + page_access_token
    print "posting to %s at url http://facebook.com/%s" % (page_name, page_id)
    path_string = "%s/feed" % page_id
    page_graph = GraphAPI(page_access_token)
    image_url = upload_link_url
    r = page_graph.post(path=path_string, link=upload_link_url) #, caption="Loksatta Revelation - June 9th, 1 pm, Press Club, Cubbon Park")
    link_id = r['id'] 
    print 'Success: posted link with id: ' + link_id
    upload_hash[page_id] = link_id
  except:
    print "Unexpected error:", sys.exc_info()[0]
    dump_file()

  count += 1
  sleep_interval = randint(1,3)
  time.sleep(sleep_interval)
  if (count > 200):
    break

copyfile(upload_history_file, upload_history_file + ".bk")
new_file = dump_file()
copyfile(new_file, upload_history_file)
