#!/bin/bash

cd /home/ubuntu/lokal/src/twitter/bin

/usr/bin/python /home/ubuntu/lokal/src/twitter/bin/get_search_results.py "bbmpadmn" 0
/usr/bin/python /home/ubuntu/lokal/src/twitter/bin/get_search_results.py "cpblr" 0
/usr/bin/python /home/ubuntu/lokal/src/twitter/bin/get_search_results.py "rk_misra" 0
/usr/bin/python /home/ubuntu/lokal/src/twitter/bin/get_search_results.py "bbmp" 0
/usr/bin/python /home/ubuntu/lokal/src/twitter/bin/get_search_results.py "aapbangalore" 0
/usr/bin/python /home/ubuntu/lokal/src/twitter/bin/get_search_results.py "bpacofficial" 0

/usr/bin/python /home/ubuntu/lokal/src/twitter/bin/target_ward_mentions.py "cpblr" 0
/usr/bin/python /home/ubuntu/lokal/src/twitter/bin/target_ward_mentions.py "bbmpadmn" 0
/usr/bin/python /home/ubuntu/lokal/src/twitter/bin/target_ward_mentions.py "rk_misra" 0
/usr/bin/python /home/ubuntu/lokal/src/twitter/bin/target_ward_mentions.py "bbmp" 0
/usr/bin/python /home/ubuntu/lokal/src/twitter/bin/target_ward_mentions.py "aapbangalore" 0
/usr/bin/python /home/ubuntu/lokal/src/twitter/bin/target_ward_mentions.py "bpacofficial" 0
/usr/bin/python /home/ubuntu/lokal/src/twitter/bin/target_ward_mentions.py "TrafflineBLORE" 0
/usr/bin/python /home/ubuntu/lokal/src/twitter/bin/target_ward_mentions.py "onlineBESCOM" 0
/usr/bin/python /home/ubuntu/lokal/src/twitter/bin/target_ward_mentions.py "blrcitypolice" 0
