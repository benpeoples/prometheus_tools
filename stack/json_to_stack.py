#!/usr/bin/python

import stack_pb2

import sys
import time

import struct
import ctypes

import binascii
import json

from sets import Set


if(len(sys.argv) < 3):
    print "Usage: json_to_stack.py stack.json stack.bin"
    sys.exit(0)

with open(sys.argv[1]) as data_file:
    data = json.load(data_file)

version = data['version']
stack_count = len(data['cuestacks'])

print "Stacks: ", stack_count

all_cuestacks = Set()

has_error = False

###validate run
for cue in data['cuestacks']:
    print json.dumps(cue)

if(has_error):
    print "Errors reported, quitting."
    sys.exit(-1)

### Real run

print "Building File!"

f = open(sys.argv[2],"wb")

f.write(bytearray(b'\x04\x4E\x01')); # Header

f.write(struct.pack("!B",data['version']))

f.write(struct.pack("!H",stack_count)) # Stack count

# Next !H is the length the cuestack, which we need to go generate first.

#stackstring = ""

for cue in data['cuestacks']:
    cuestring = ""

    cuestack = stack_pb2.CueStack()
    cuestack.cuestack_id = cue['cuestack_id']
    if('label' in cue):
        cuestack.label = cue['label']
    if('loop' in cue):
        cuestack.loop = cue['loop']
    serialized = cuestack.SerializeToString()
    length = len(serialized)
    cuestring += struct.pack("!B",length)  # Write the length of this bit
    cuestring += serialized # then the data

    for cuestep in cue['cuesteps']:
        wait = cuestep['wait']
        fix_count = len(cuestep['fixtures'])
        cuestring += struct.pack('!I',wait)
        cuestring += struct.pack('!H',fix_count)
        for cf in cuestep['fixtures']:
            cuefix = stack_pb2.CueFix()
            cuefix.fixture_id = cf['fixture_id']
            if('fade' in cf):
                cuefix.fade = cf['fade']
            else:
                cuefix.fade = wait

            if('intensity' in cf['color']):
                cuefix.color.intensity = cf['color']['intensity']
            if('red' in cf['color']):
                cuefix.color.red = cf['color']['red']
            if('green' in cf['color']):
                cuefix.color.green = cf['color']['green']
            if('blue' in cf['color']):
                cuefix.color.blue = cf['color']['blue']
            if('white' in cf['color']):
                cuefix.color.white = cf['color']['white']
            if('cool' in cf['color']):
                cuefix.color.cool = cf['color']['cool']
            if('warm' in cf['color']):
                cuefix.color.warm = cf['color']['warm']

            cuefix_string = cuefix.SerializeToString()
            cuefix_length = len(cuefix_string) # Max 56

            cuestring += struct.pack("!B",cuefix_length)
            cuestring += cuefix_string

    length = len(cuestring)
    f.write(struct.pack('!H',length))
    f.write(cuestring)

#f.write(struct.pack('!I',len(stackstring)))
#f.write(stackstring)


print "Done!"

f.close()
