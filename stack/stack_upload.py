#!/usr/bin/env python

import socket
import sys
import time
import os
import struct

TCP_IP = sys.argv[1]
TCP_PORT = 1234
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
# 7ceeaf4b-7be9-4bab-b03c-4c733418f3dc
s.send(b'\xe5\x1b\xbc\xa3\x02')

filesize = os.path.getsize(sys.argv[2])

print filesize

s.send(struct.pack('!I',filesize))

with open(sys.argv[2],'rb') as f:
          for line in f:
              try:
                  s.send(line)
                  sys.stdout.write('.')
                  sys.stdout.flush()
                  #time.sleep(0.1)
              except (socket.error):
                  print "err"
                  time.sleep(0.5)
s.close()
sys.stdout.write('\n')
