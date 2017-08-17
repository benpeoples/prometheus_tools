#!/usr/bin/python

import patch_pb2

import sys
import time

import struct
import ctypes

import binascii
import json

from sets import Set
#from array import array




if(len(sys.argv) < 3):
    print "Usage: patch_to_json.py patch.bin patch.json"
    sys.exit(0)

f = open(sys.argv[1],"rb")

header = f.read(4)

if(header != bytearray(b'\x04\x4E\x02\x00')):
    print "Not a patch file!"
    f.close()
    sys.exit(-1)

data = []

fixture_count = struct.unpack("!H",f.read(2))[0]

print "Fixture count: ", fixture_count

for n in range(fixture_count):
    length = struct.unpack("!B",f.read(1))[0]
    serialized = f.read(length)
    fixture = patch_pb2.fixture()
    fixture.ParseFromString(serialized)
    print fixture
    fix = {
    'fixture_id' : fixture.fixture_id,
    'fixture_type' : fixture.fixture_type,
    'start_address' : fixture.start_address
    }

    #if person.HasField('email'):
    if fixture.HasField('num_channels'):
        fix['num_channels'] = fixture.num_channels
    if fixture.HasField('label'):
        fix['label'] = fixture.label
    if fixture.HasField('vw_cool'):
        fix['vw_cool'] = fixture.vw_cool
    if fixture.HasField('vw_warm'):
        fix['vw_warm'] = fixture.vw_warm
    if fixture.HasField('channel_map'):
        fix['channel_map'] = []
        channel_map = list(fixture.channel_map)
        for i in channel_map:
            fix['channel_map'].append(ord(i))


    data.append(fix)


f.close()


json_string = json.dumps(data, indent=4, sort_keys=True)

print json_string

json_output = open(sys.argv[2], "w")

json_output.write(json_string)

json_output.close()
