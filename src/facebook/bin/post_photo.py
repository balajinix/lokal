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
upload_history_file = "../logs/blt_city_government.txt"
log_file = "../logs/post_photo.log"
upload_photo_url = 'http://loksattakarnataka.org/wp-content/uploads/2015/06/5-20-1000-Bengaluru-Needs-No-Charity-A4x2.jpg'

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
    try:
      ward_name = page_name.replace("Loksatta ", "")
      upload_photo_caption = "Bengaluru needs a City Government, not charity from CM. We want,\n\n1. Empowered MPC (Metropolitan Plann#ing Committee).\n2. Directly elected Mayor with 5 year term.\n3. Ward Committees in each ward.\n4. Give 10%% of taxes collected from Bengaluru back to the city (about Rs. 7000 crores per annum).\n\nInstead, the CM wants to give Bengaluru a makeover with Rs. 3500 crores of tax payers money just before the BBMP elections. http://www.deccanherald.com/content/481293/government-draws-up-ambitious-plan.html\n\nDo we need such charity or an empowered city government?\n\nDo you know if the Ward Committee in your area ever met? If not, why?\n\nWhy is the BBMP woefully short of funds unlike Mumbai or Hyderabad city governments?\n\nWhy do we have rotating mayors with short 1 years terms?"
      print upload_photo_caption
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
