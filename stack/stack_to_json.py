#!/usr/bin/python

import stack_pb2

import sys
import time

import struct
import ctypes

import binascii
import json

from sets import Set
#from array import array

if(len(sys.argv) < 3):
    print "Usage: stack_to_json.py stack.bin stack.json"
    sys.exit(0)

f = open(sys.argv[1],"rb")

header = f.read(3)

if(header != bytearray(b'\x04\x4E\x01')):
    print "Not a stack file!"
    f.close()
    sys.exit(-1)

data = {}

stack_version = struct.unpack('!B',f.read(1))[0]

data['version'] = stack_version

print "Stack version:", stack_version

data['cuestacks'] = []

stack_count = struct.unpack("!H",f.read(2))[0]

print "Stack count: ", stack_count

for n in range(stack_count):
    stack_length = struct.unpack("!H",f.read(2))[0]
    print "Total Stack Length: ", stack_length
    stack_ptr = f.tell()
    length = struct.unpack("!B", f.read(1))[0]
    print "Cuestack Len", length
    serialized = f.read(length)
    cuestack = stack_pb2.CueStack()
    cuestack.ParseFromString(serialized)
    print cuestack
    cs = {
    'cuestack_id' : cuestack.cuestack_id
    }

    if cuestack.HasField('label'):
        cs['label'] = cuestack.label
    if cuestack.HasField('loop'):
        cs['loop'] = cuestack.loop
    else:
        cs['loop'] = False

    cs["cuesteps"] = []

    while ((stack_ptr + stack_length) > f.tell()):
        step = {}
        wait = struct.unpack('!I',f.read(4))[0]
        fix_count = struct.unpack('!H',f.read(2))[0]

        print "Wait: ", wait
        print "Fix_Count: ", fix_count

        step['wait'] = wait

        step['fixtures'] = []

        for q in range(fix_count):
            length = struct.unpack("!B", f.read(1))[0]
            serialized = f.read(length)
            cuefix = stack_pb2.CueFix()
            cuefix.ParseFromString(serialized)
            cf = {}
            cf['fixture_id'] = cuefix.fixture_id
            cf['fade'] = cuefix.fade
            cf['color'] = {}
            if cuefix.color.HasField('intensity'):
                cf['color']['intensity'] = cuefix.color.intensity
            if cuefix.color.HasField('red'):
                cf['color']['red'] = cuefix.color.red
            if cuefix.color.HasField('green'):
                cf['color']['green'] = cuefix.color.green
            if cuefix.color.HasField('blue'):
                cf['color']['blue'] = cuefix.color.blue
            if cuefix.color.HasField('white'):
                cf['color']['white'] = cuefix.color.white
            if cuefix.color.HasField('cool'):
                cf['color']['cool'] = cuefix.color.cool
            if cuefix.color.HasField('warm'):
                cf['color']['warm'] = cuefix.color.warm

            step['fixtures'].append(cf)
        cs["cuesteps"].append(step)


    data['cuestacks'].append(cs)



f.close()


json_string = json.dumps(data, indent=4, sort_keys=True)

print json_string

json_output = open(sys.argv[2], "w")

json_output.write(json_string)

json_output.close()
