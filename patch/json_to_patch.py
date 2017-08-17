#!/usr/bin/python

import patch_pb2

import sys
import time

import struct
import ctypes

import binascii
import json

from sets import Set


if(len(sys.argv) < 3):
    print "Usage: json_to_patch.py patch.json patch.bin"
    sys.exit(0)

with open(sys.argv[1]) as data_file:
    data = json.load(data_file)



fixture_count = len(data)

print "Fixtures: ", fixture_count

#f.write(bytearray(b'\x04\x4E\x02\x00')); # Header

#f.write(struct.pack("!H",fixture_count)) # Fixture count

all_fixtures = Set()

has_error = False

###validate run
for fix in data:
    print json.dumps(fix)
    if('fixture_id' not in fix):
        print "ERROR: Need fixture_id"
        has_error = True
    if('start_address' not in fix):
        print "ERROR: Need start_address"
        has_error = True
    if('fixture_type' not in fix):
        print "ERROR Need fixture_type"
        has_error = True

    if('fixture_id' in fix):
        if(fix['fixture_id'] in all_fixtures):
            print "ERROR: Duplicate Fixture ID: ", fix['fixture_id']
            has_error = True
        all_fixtures.add(fix['fixture_id'])

if(has_error):
    print "Errors reported, quitting."
    sys.exit(-1)

### Real run

print "Building File!"

f = open(sys.argv[2],"wb")

f.write(bytearray(b'\x04\x4E\x02\x00')); # Header

f.write(struct.pack("!H",fixture_count)) # Fixture count

for fix in data:
    fixture = patch_pb2.fixture()
    fixture.fixture_id = fix['fixture_id']
    fixture.fixture_type = fix['fixture_type']
    fixture.start_address = fix['start_address']
    if('num_channels' in fix):
        fixture.num_channels = fix['num_channels']
    if('label' in fix):
        fixture.label = fix['label'][0:20]
    if('vw_cool' in fix):
        fixture.vw_cool = fix['vw_cool']
    if('vw_warm' in fix):
        fixture.vw_cool = fix['vw_warm']
    if('channel_map' in fix):
        if(2 in fix['channel_map'] and 3 in fix['channel_map'] and 4 in fix['channel_map']):
            fixture.rgb = True;
        if(1 in fix['channel_map']):
            fixture.intensity = True;
        if(6 in fix['channel_map'] and 7 in fix['channel_map']):
            fixture.vw = True;
#        if(5 in fix['channel_map']):
#            fixture.white = True;
        fixture.channel_map = str(bytearray(fix['channel_map']))
    print fixture
    serialized = fixture.SerializeToString()
    length = len(serialized)
    print length
    f.write(struct.pack("!B",length))
    f.write(serialized)

print "Done!"

f.close()
