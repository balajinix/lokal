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
upload_history_file = "../logs/denque.txt"
#upload_history_file = "../logs/coming_soon.txt"
log_file = "../logs/post_photo.log"
upload_photo_url = 'http://loksattakarnataka.org/wp-content/uploads/2015/05/11264838_10205764583449480_8524941219634272852_n.jpg'
#upload_photo_url = 'http://loksattakarnataka.org/wp-content/uploads/2015/05/LSPK-Announcement.png'

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

  # ignore pages that we don't want updated
  #if page_name == 'Bengaluru LOKal' or page_name == 'Loksatta for BBMP' or page_name == 'Ashwin4MLA' or page_name == 'Ashwin4MLC':
  #  continue

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
    #upload_photo_caption = "Loksatta Promise: If our candidate becomes councilor for %s in BBMP, we'll make and keep all drain manhole covers level with the road.\n\nWhy are drain manhole covers on Bengaluru roads, not level with the road surface? Loksatta's National Vice President Dr. Ashwin Mahesh explains in the below link.\n\nhttps://www.facebook.com/photo.php?fbid=10205804666091521&set=a.2097391670050.2122376.1103113024&type=1&permPage=1\n\nIn one word: Corruption. We'll fix this.\n\nHence this pledge: If Loksatta wins the BBMP Councilor election from %s, we promise to make and then keep, all drain manhole covers level with the road.\n\nYou can access more Loksatta solutions for a better Bengaluru here: http://loksattakarnataka.org/BengaluruLokal" % (page_name.replace("Loksatta ",""), page_name.replace("Loksatta ",""))
    try:
      upload_photo_caption = "Dengue comes every year. Can the solution come this year?\n\nBengaluru needs a Health Map to combat Dengue. When elected to BBMP, Loksatta Party councillors will work wth the city government to publish the number of patients treated each day of the year and the diseases diagnosed at every hospital in Bengaluru. Patient information anonymized ofcourse. This data will form a Health Map to predict future epidemics, as well as to critically analyze the performance of public hospitals.\n\nWe request %s volunteers to come up suggestions to combat Denque and other epidemics in your area. This could be things like cleaning a open drain or ensuring adequate medical supplies at a public hospital or working with private doctors in your area and seeking guidance from them. Together with your ward coordinator and Loksatta candidate for BBMP, we can make a real impact on the health of people in your ward.\n\nYou can access more Loksatta solutions for a better Bengaluru here: http://loksattakarnataka.org/BengaluruLokal." % (page_name)
    except:
      print "Error in caption"
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
