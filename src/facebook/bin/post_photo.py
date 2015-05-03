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
upload_history_file = "../input/land_grabbing.txt"
#upload_photo_url = 'http://4.bp.blogspot.com/-BLWWSEmKcoI/VTNOMewzPXI/AAAAAAAAB6I/P_YpCc4xjfk/s1600/LOKal%2BOne-Sheeter.jpg'
#upload_photo_url = 'http://1.bp.blogspot.com/-j2cvkQVWFVM/VTkVR0gbxLI/AAAAAAAAB6w/ko4If9Gh4A8/s1600/Wanted%2BPoster-rev.jpg'
#upload_photo_url = 'http://3.bp.blogspot.com/-CggBxiyUp-Q/VULPkzfxeAI/AAAAAAAAB7c/t3KU5-DpEGw/s1600/Red%2BCarpet.png'
#upload_photo_caption = "Bengaluru LOKal platform is ready. The carpet's rolled out. Are you ready to participate? If YES, let us know here: http://goo.gl/forms/Q4XwKbeyoA"
upload_photo_url = 'http://1.bp.blogspot.com/-Geytv-dcfDY/VULZOjMmF7I/AAAAAAAAB7s/YsPjauxqXz0/s1600/Labour%2BDay_pourakarmikas.jpg'
upload_photo_url = 'http://4.bp.blogspot.com/-7NRe8Hf7A6U/VUQ2RioSDzI/AAAAAAAAB8I/rSd8ciNo6EE/s1600/11125267_10153884723284832_6666883335278704733_o.jpg'


upload_hash = {}
def dump_file():
  timestamp = datetime.datetime.now().time().isoformat()
  new_file = upload_history_file + "_" + timestamp
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
  # we need to provide a file name to keep track of photo ids
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
      photo_id = parts[1]
      if page_id not in upload_hash:
        upload_hash[page_id] = photo_id
  f.close()
except:
  print "File not found: %s" % (upload_history_file)
      

graph = GraphAPI(access_token)
response = graph.get("/100004978365543/accounts")
pages = response['data']
count = 0
for page in pages:
  page_name = page['name']
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
    path_string = "%s/photos" % page_id
    page_graph = GraphAPI(page_access_token)
    image_url = upload_photo_url
    upload_photo_caption = 'We request %s volunteers to join the protest march today, against land grabbing, supported by Loksatta Party Karnataka.' % (page_name)
    r = page_graph.post(path=path_string,caption=upload_photo_caption,source=urllib2.urlopen(image_url))
    photo_id = r['id'] 
    print 'Success: posted photo with id: ' + photo_id
    upload_hash[page_id] = photo_id
  except:
    print "Could not upload photo to page %s with id: %s and access_token: %s" % (page_name, page_id, access_token)
    dump_file()
  count += 1
  sleep_interval = randint(1,3)
  time.sleep(sleep_interval)
  if (count > 200):
    break

copyfile(upload_history_file, upload_history_file + ".bk")
new_file = dump_file()
copyfile(new_file, upload_history_file)
