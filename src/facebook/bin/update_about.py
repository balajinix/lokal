#! /usr/bin/env python

from facepy import GraphAPI
import sys
import urllib
import urllib2

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
pages = response['data']
for page in pages:
  page_name = page['name']
  if (page_name == 'Ashwin4MLA' or
     page_name == 'Loksatta for BBMP'):
    continue
  page_id = page['id']
  page_access_token = page['access_token']
  #print page_name + '\t' + page_id + '\t' + page_access_token
  if (page_name == 'Loksatta Padarayanapura'):
    print page_name + '\t' + page_id + '\t' + page_access_token
    print "posting to http://facebook.com/%s" % (page_id)
    #image_url = "https://www.facebook.com/photo.php?fbid=462826560559952"

    page_graph = GraphAPI(page_access_token)

    # cover
    path_string = "%s" % page_id
    #r = page_graph.post(cover=462826560559952)
    r = page_graph.post(path=path_string, about="LOKal 135")
    #LOKal 135, Loksatta Padarayanapura, BBMP Ward 135, Bengaluru.
    print r

    # post photo
    #path_string = "%s/photos" % page_id
    #image_url = 'https://twitter.com/LoksattaBBMP/status/589382119488499712/photo/1'
    #r = page_graph.post(path=path_string,source=urllib2.urlopen(image_url))

    # post message
    #path_string = "%s/feed" % page_id
    #r = page_graph.post(path=path_string,message="Test message")

    #print r
    break
  else:
    continue
  break
