#!/usr/bin/python

import time_pb2

import sys
import time

import struct
import ctypes

import binascii
import json

import bitstruct

from sets import Set


if(len(sys.argv) < 3):
    print "Usage: json_to_trigger.py trigger.json trigger.bin"
    sys.exit(0)

with open(sys.argv[1]) as data_file:
    data = json.load(data_file)

trigger_count = len(data)

print "Triggers: ", trigger_count

#f.write(bytearray(b'\x04\x4E\x02\x00')); # Header

#f.write(struct.pack("!H",fixture_count)) # Fixture count

all_triggers = Set()

has_error = False

###validate run
for time in data:
    print json.dumps(time)
    if('trigger_id' not in time):
        print "ERROR: Need trigger_id"
        has_error = True

    if('trigger_id' in time):
        if(time['trigger_id'] in all_triggers):
            print "ERROR: Duplicate Trigger ID: ", time['trigger_id']
            has_error = True
        all_triggers.add(time['trigger_id'])

if(has_error):
    print "Errors reported, quitting."
    sys.exit(-1)

### Real run

print "Building File!"

f = open(sys.argv[2],"wb")

f.write(bytearray(b'\x04\x4E\x03\x00')); # Header

f.write(struct.pack("!H",trigger_count)) # Fixture count

for time in data:
    trigger = time_pb2.TimeTrigger()
    trigger.trigger_id = time['trigger_id']
    if('start_month' in time and 'start_day' in time):
        trigger.start_date = struct.unpack("!I",struct.pack("!HH",time['start_month'],time['start_day']))[0]
    if('end_month' in time and 'end_day' in time):
        trigger.end_date = struct.unpack("!I",struct.pack("!HH",time['end_month'],time['end_day']))[0]
    if('day_of_week' in time):
        trigger.day_of_week = struct.unpack("!B",bitstruct.pack("p1b1b1b1b1b1b1b1",time['day_of_week'][0],time['day_of_week'][1],time['day_of_week'][2],time['day_of_week'][3],time['day_of_week'][4],time['day_of_week'][5],time['day_of_week'][6]))[0]
    if('start_type' in time):
        trigger.start_type = time['start_type']
    if('end_type' in time):
        trigger.end_type = time['end_type']
    if('start' in time):
        trigger.start = time['start']
    if('end' in time):
        trigger.end = time['end']
    if('priority' in time):
        trigger.priority = time['priority']
    if('action' in time):
        trigger.action = time['action']

    print trigger
    serialized = trigger.SerializeToString()
    length = len(serialized)
    print length
    f.write(struct.pack("!B",length))
    f.write(serialized)

print "Done!"

f.close()
