#! /usr/bin/env python

# Author - Balaji Ganesan
# Email - balajinix@gmail.com

import twitter

import datetime
import time
from shutil import copyfile
import sys
import time
from random import randint

# make sure you run the script with debug set to True first
debug = True

categories = {
              'pourakarmika' : 'pourakarmika',
              'bwssb' : 'bwssb',
              'sewage' : 'bwssb',
              'garbage' : 'garbage',
              'cleaning' : 'garbage',
              'police' : 'police',
              'CPBlr' : 'police',
              'BlrCityPolice' : 'police',
              'footpath' : 'footpath',
              'tanker' : 'water',
              'contractor' : 'bbmp',
              'traffic' : 'traffic',
              'hsr' : '174',
              'bellandur' : '150',
              'flood' : 'flood',
              'lake' : 'lakes',
              'dengue' : 'dengue'
             }

messages = {
             'pourakarmika' : 'Loksatta supports better working conditions for Pourakarmikas.',
             'flood' : 'Bengaluru needs a flood-resilience strategy proposed by Dr. @ashwinmahesh',
             'footpath' : 'Loksatta demands usable footpaths on all roads. Prioritize Pedestrians!',
             'lake' : 'Loksatta supports Lake rejuvenation to solve Bengaluru water crisis.',
             'dengue' : 'Loksatta demands a Health Map to combat Dengue in Bengaluru.',
             'water' : 'Loksatta demands tanker water tariff be same as pipe water tariff.',
             'garbage' : 'Loksatta demands SWM and Segregation of waste by BBMP. Dumping Saaku!'
           }

# we need to have proper credentials
consumer_key = ''
consumer_secret = ''
access_token_key = ''
access_token_secret = ''
try:
  with open('../input/access_token.txt') as f:
    lines = f.readlines()
    if len(lines) != 4:
      print "access_token file should have four lines. lines_count: ", len(lines)
      sys.exit()
    consumer_key = lines[0].strip().split('\t')[1]
    consumer_secret = lines[1].strip().split('\t')[1]
    access_token_key = lines[2].strip().split('\t')[1]
    access_token_secret = lines[3].strip().split('\t')[1]
except:
  print "Error geting access token"
  sys.exit()

# initialize the module
api = twitter.Api(consumer_key, consumer_secret, access_token_key, access_token_secret)

# we don't want to tweet again and again to same people
# so store a history of people tweeted to
upload_history_file = "../logs/twitter_campaign.txt"
upload_hash = {}
def dump_file():
  timestamp = datetime.datetime.now().time().isoformat()
  new_file = upload_history_file + "_" + timestamp
  f = open(new_file, 'w')
  for k, v in upload_hash.iteritems():
    f.write(k + '\t' + v + '\n')
  f.close()
  return new_file
# load history file onto hash
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
   
search = api.GetSearch(term='bbmpadmn', lang='en', result_type='recent', count=200, max_id='')
append_url = " http://loksattakarnataka.org/BengaluruLokal/"
append_handle = " Join @BengaluruLOKal"
for t in search:
  #print t.user.screen_name + ' (' + t.created_at + ')'
  screen_name = t.user.screen_name

  # for now, we'll not tweet to those already tweeted to
  if screen_name in upload_hash:
    print "Already tweeted to", screen_name, " with message ", upload_hash[screen_name]
    continue

  #Add the .encode to force encoding
  tweet = t.text.encode('utf-8')

  # lets see if there is any category
  tweet_category = ''
  for k, v in categories.iteritems():
    if k in tweet.lower():
      #tweet_category += v + '|'
      tweet_category = v
  if len(tweet_category) < 1:
    continue

  if tweet_category in messages:
    base_response = "@" + t.user.screen_name + " " + messages[tweet_category]
    response = base_response
    #if len(response) + len(append_url) < 140:
    response += append_url
    #if len(response) + len(append_handle) < 140:
    response += append_handle
    try:
      if debug == False:
        print "Tweet: ", screen_name, tweet
        print "Category: ", tweet_category
        print "Response: ", response, len(response)
        #status = api.PostUpdate(response)
    except Exception, e:
      response = base_response
      try:
        print "Retry Response: ", response, len(response)
        #if debug == False:
          #status = api.PostUpdate(response)
      except Exception, e:
        "[Error] Could not tweet response %s" %(response)
    if debug == False:
      upload_hash[screen_name] = messages[tweet_category]
    sleep_interval = randint(1,3)
    time.sleep(sleep_interval)

if debug == False:
  copyfile(upload_history_file, upload_history_file + ".bk")
  new_file = dump_file()
  copyfile(new_file, upload_history_file)
