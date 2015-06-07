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

if len(sys.argv) != 3:
  print "Usage: %s <search_term> <debug_mode>\n"
  sys.exit()

search_term = sys.argv[1]
debug_mode = sys.argv[2]
# make sure you run the script with debug set to True first
debug = True
if debug_mode == '0':
  debug = False

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
upload_history_file = "../logs/ward_invites.txt"
upload_hash = {}
def dump_file():
  timestamp = datetime.datetime.now().time().isoformat()
  new_file = upload_history_file + "_" + timestamp
  f = open(new_file, 'w')
  for k, v in upload_hash.iteritems():
    f.write(k + '\t' + v + '\n')
  f.close()
  return new_file

# load ward info file
ward_file = "../input/bbmp_wards.txt"
ward_name_hash = {}
ward_num_hash = {}
ward_num_name_mapping = {}
try:
  # we need to provide a file name to keep track of photo ids
  with open(ward_file) as f:
    lines = f.readlines()
    for line in lines:
      line = line.strip()
      parts = line.split('\t')
      if len(parts) != 3:
        print "Error reading ward info file"
        print line
        continue
      ward_num = parts[0]
      ward_name = parts[1]
      ward_name_key = ward_name.lower()
      ward_url= parts[2]
      if ward_name_key not in ward_name_hash:
        ward_name_hash[ward_name_key] = ward_url 
      if ward_num not in ward_num_hash:
        ward_num_hash[ward_num] = ward_url 
      if ward_num not in ward_num_name_mapping:
        ward_num_name_mapping[ward_num] = ward_name

  f.close()
except:
  print "File not found: %s" % (upload_history_file)

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
   
search = api.GetSearch(term=search_term, lang='en', result_type='recent', count=1000, max_id='')
for t in search:
  #print t.user.screen_name + ' (' + t.created_at + ')'
  screen_name = t.user.screen_name

  # for now, we'll not tweet to those already tweeted to
  if screen_name in upload_hash:
    #print "Already tweeted to", screen_name, " with message ", upload_hash[screen_name]
    continue

  #Add the .encode to force encoding
  tweet = t.text.encode('utf-8')

  # lets see if there is any ward info
  tweet_words = tweet.split(' ')
  ward_score = 0
  for word in tweet_words:
    word = word.lower()
    if word in ward_name_hash:
      print word, "is a ward name"
      ward_name = word
      ward_url = ward_name_hash[ward_name]
      ward_score += 1
    if 'ward' in tweet and word == '171':
      print word.isdigit(), " is a ward number"
      if word in ward_num_hash:
        print word, ward_num_hash[word]
      if word.isdigit() == True and word in ward_num_hash:
        ward_name = ward_num_name_mapping[word]
        ward_url = ward_num_hash[word]
        ward_score += 1
        break

  if ward_score > 0:
    response = "@" + t.user.screen_name + " Become a problem solver in %s. Join our LOKal team. %s" % (ward_name.title(), ward_url)
    try:
      mention = "Tweet: @" + screen_name + " says: " + tweet
      print mention
      if debug is False:
        status = api.PostUpdate(response)
      print "Response: ", response, "\n"
    except Exception, e:
      print "[Error] Could not tweet response %s" %(response)
    if debug is False:
      upload_hash[screen_name] = ward_name.title()
      sleep_interval = randint(5, 25)
      time.sleep(sleep_interval)

if debug is False:
  copyfile(upload_history_file, upload_history_file + ".bk")
  new_file = dump_file()
  copyfile(new_file, upload_history_file)
