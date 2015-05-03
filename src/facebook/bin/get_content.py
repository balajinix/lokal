#! /usr/bin/env python
from urllib2 import urlopen
from simplejson import loads
content = loads(urlopen('http://graph.facebook.com/100004978365543').read())
print content
