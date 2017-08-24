#!/Library/Frameworks/Python.framework/Versions/2.7/Resources/Python.app/Contents/MacOS/Python

from cmd2 import Cmd
import socket
import time
from IPy import IP
import struct
import random
import os
import sys
import pprint
import varint

import pm_proto_pb2

PM_DISC_PORT = 1557
PM_PROTO_PORT = 1102

"""
dim : "single channel dimmer"
type = 1
num_channels = 1
intensity = true
vw = false
rgb = false
channel_map = 0x01 0x00...

rgb : "3-channel rgb fixture"
type = 2
num_chnanels = 3
intensity = false
vw = false
rgb = true
channel_map = 0x02 0x03 0x04 0x00...

rgbw : "4-channel rgbw fixture"
type = 3
num_chnanels = 4
intensity = false
vw = false
rgb = true
channel_map = 0x02 0x03 0x04 0x05 0x00...

vw : "2-channel vw fixture"
type = 4
num_chnanels = 2
intensity = false
vw = true
rgb = false
channel_map = 0x06 0x07 0x00 0x00 0x00...

gantom_precision : "Gantom 7-channel Precision DMX"
type = 41
num_chnanels = 7
intensity = false
vw = false
rgb = true
channel_map = 0x02 0x03 0x04 0x00 0x00...
"""

fixture_types = {
'dim' : {'label' : 'Single Channel Dimmer', 'type' : 1, 'num_channels' : 1, 'intensity' : True, 'vw' : False, 'rgb' : False, 'channel_map' : '\x01\x00'},
'rgb' : {'label' : 'Generic 3-channel RGB', 'type' : 2, 'num_channels' : 3, 'intensity' : False, 'vw' : False, 'rgb' : True, 'channel_map' : '\x02\x03\x04'},
'rgbw' : {'label' : 'Generic 4-channel RGBW', 'type' : 3, 'num_channels' : 4, 'intensity' : False, 'vw' : False, 'rgb' : True, 'channel_map' : '\x02\x03\x04\x05'},
'vw' : {'label' : 'Generic 2-channel VW', 'type' : 4, 'num_channels' : 2, 'intensity' : False, 'vw' : True, 'rgb' : False, 'channel_map' : '\x06\x07'},
'gantom_precision' : {'label' : 'Gantom 7-channel Precision DMX', 'type' : 5, 'num_channels' : 7, 'intensity' : False, 'vw' : False, 'rgb' : True, 'channel_map' : '\x02\x03\x04\x00\x00\x00\x00\x00'}
}

def is_float(string):
  try:
    return float(string) and '.' in string  # True if string is a number with a dot
  except ValueError:  # if string is not a number
    return False

def socket_read_n(sock, n):
    """ Read exactly n bytes from the socket.
        Raise RuntimeError if the connection closed before
        n bytes were read.
    """
    buf = ''
    while n > 0:
        data = sock.recv(n)
        if data == '':
            raise RuntimeError('unexpected connection close')
        buf += data
        n -= len(data)
    return buf

def decode_socket(stream):
    """Read a varint from `stream`"""
    shift = 0
    result = 0
    while True:
        i = struct.unpack("!B",stream.recv(1))[0]
        result |= (i & 0x7f) << shift
        shift += 7
        if not (i & 0x80):
            break

    return result

def transact_message(msg):
    global prometheus_ip
    if prometheus_ip is not None:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((str(prometheus_ip),PM_PROTO_PORT))
        packed_len = varint.encode(len(msg))
        print len(msg)
        s.send(packed_len + msg)
        try:
            s.settimeout(1.0)
            msg_len = decode_socket(s)
            msg_buf = socket_read_n(s, msg_len)
            return msg_buf
        except:
            return None
    else:
        print "Connect first!"

def ping_pm():
    message = pm_proto_pb2.pmproto()
    message.type = pm_proto_pb2.pmproto.PING
    msg = message.SerializeToString()
    if transact_message(msg) is not None:
        return True
    else:
        return False




def create_connection(ip_address):
        global prometheus_ip
        message = pm_proto_pb2.pmproto()
        message.type = pm_proto_pb2.pmproto.PING
        print "Connecting to ", ip_address
        print message
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((str(ip_address),PM_PROTO_PORT))
        msg = message.SerializeToString()
        print "sending", len(msg), "bytes"
        packed_len = varint.encode(len(msg))
        print "sent", s.send(packed_len + msg), "bytes"

        #s.sendto("hello",(ip_address,PM_PROTO_PORT))

        #try:
        if True:
            s.settimeout(1.0)
            msg_len = decode_socket(s)
            msg_buf = socket_read_n(s, msg_len)
            message.ParseFromString(msg_buf)
            print "Got", len(msg_buf), "bytes"
            print "Msg len: ", msg_len
            print message
            print msg_len
            if(message.type != pm_proto_pb2.pmproto.PING):
                prometheus_ip = ip_address

        else:
            print "No response!"
        s.settimeout(None)


# From http://thoughtsbyclayg.blogspot.com/2008/10/parsing-list-of-numbers-in-python.html
def parseIntSet(nputstr=""):
  selection = set()
  invalid = set()
  # tokens are comma seperated values
  tokens = [x.strip() for x in nputstr.split(',')]
  for i in tokens:
     try:
        # typically tokens are plain old integers
        selection.add(int(i))
     except:
        # if not, then it might be a range
        try:
           token = [int(k.strip()) for k in i.split('-')]
           if len(token) > 1:
              token.sort()
              # we have items seperated by a dash
              # try to build a valid range
              first = token[0]
              last = token[len(token)-1]
              for x in range(first, last+1):
                 selection.add(x)
        except:
           # not an int and not a range...
           invalid.add(i)
  # Report invalid tokens before returning valid selection
  #print "Invalid set: " + str(invalid)
  return selection
# end parseIntSet


quotes = ["""O dear Ophelia!
I am ill at these numbers:
I have not art to reckon my groans.""","""There wanted not some beams of light
to guide men in the exercise of their Stocastick faculty.""","""By means of the thread one understands the ball of yarn,
so we'll be satisfied and assured by having this sample.""","""If the numbers are not random,
they are at least higgledy-piggledy.""","""Attempt the end and never stand to doubt;
Nothing's so hard, but search will find it out.""","""Always palletize your color! - CTW"""]

colors = {}

def parse_intensity(int_string):
    if(int_string[-1] == '%'):
        return int(int(int_string[0:-1])*65535/100)
    else:
        return int(int_string)

def parse_color(color_string,color_type):
    if(color_type == 0): #RGB
        if color_string in colors:
            if 'rgb' in colors[color_string]:
                return (colors[color_string]['rgb'][0] << 16) + (colors[color_string]['rgb'][1] << 8) + (colors[color_string]['rgb'][2])


def print_fix_line(start,end):
    for f in range(start,end):
        if f in fix_patch:
            if fix_patch[f].captured:
                sys.stdout.write('\033[;7m')
            sys.stdout.write('   {0:<3} '.format(f))
            if fix_patch[f].captured:
                sys.stdout.write('\033[0;0m')
        else:
            sys.stdout.write('       ')
    sys.stdout.write('\n')
    for f in range(start,end):
        if f in fix_patch:
            if fix_patch[f].captured:
                sys.stdout.write('\033[;7m')
            sys.stdout.write('{0:06X} '.format(fix_patch[f].cRGB))
            if fix_patch[f].captured:
                sys.stdout.write('\033[0;0m')
        else:
            sys.stdout.write('       ')

    sys.stdout.write('\n')
    for f in range(start,end):
        if f in fix_patch:
            if fix_patch[f].captured:
                sys.stdout.write('\033[;7m')
            sys.stdout.write('{0:>6} '.format(fix_patch[f].intensity))
            if fix_patch[f].captured:
                sys.stdout.write('\033[0;0m')

        else:
            sys.stdout.write('       ')
    sys.stdout.write('\n')
    sys.stdout.write('\n')

def record_a_cue(the_cue,tspec,mode):
    global cue_stacks
    fix_count = 0
    if(mode == 0):
        if the_cue[0] in cue_stacks:
            cue_stacks[the_cue[0]].cuesteps[the_cue[1]] = CueStep(tspec[0],0)
            for fix in fix_patch:
                fix_count += 1
                cue_stacks[the_cue[0]].cuesteps[the_cue[1]].cue_fix.append(CueFix(fix,tspec[1]))
                cue_stacks[the_cue[0]].cuesteps[the_cue[1]].cue_fix[-1].intensity = fix_patch[fix].level
                if(fix_patch[fix].rgb):
                    cue_stacks[the_cue[0]].cuesteps[the_cue[1]].cue_fix[-1].crgb = fix_patch[fix].cRGB
            cue_stacks[the_cue[0]].cuesteps[the_cue[1]].fix_count = fix_count
        else:
            cue_stacks[the_cue[0]] = Cuestack(the_cue[0],0)
            cue_stacks[the_cue[0]].cuesteps[the_cue[1]] = CueStep(tspec[0],0)
            for fix in fix_patch:
                fix_count += 1
                cue_stacks[the_cue[0]].cuesteps[the_cue[1]].cue_fix.append(CueFix(fix,tspec[1]))
                cue_stacks[the_cue[0]].cuesteps[the_cue[1]].cue_fix[-1].intensity = fix_patch[fix].level
                if(fix_patch[fix].rgb):
                    cue_stacks[the_cue[0]].cuesteps[the_cue[1]].cue_fix[-1].crgb = fix_patch[fix].cRGB
            cue_stacks[the_cue[0]].cuesteps[the_cue[1]].fix_count = fix_count



class App(Cmd):
    """Simple command processor example."""

    prompt = 'Q0.0: '
    intro = """
Prometheus Commandline Programmer v0.0

""" + random.choice(quotes) + """

"""

    ruler = '-'

    disc_prometheus = []

    def do_open(self, line):
        print "Open " + line

    def do_save(self, line):
        print "Save " + line

    def do_delete(self, line):
        print "Delete " + line

    def do_ping(self, line):
        if ping_pm():
            print "OK"
        else:
            print "No response"

    def do_find(self, line):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('',PM_DISC_PORT))
        s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
        s.sendto("ping",('<broadcast>',PM_DISC_PORT))
        disc_prometheus = []
        while True:
            try:
                s.settimeout(2.0)
                data, addr = s.recvfrom(1024)
                #print data
                #print addr
                if(data != 'ping'):
                    self.disc_prometheus.append(addr[0])
            except:
                break
        s.settimeout(None)
        for prom in self.disc_prometheus:
            print "Found: ", prom

    def do_connect(self, line):
        which = None
        if(line == ""):
            if(len(self.disc_prometheus) == 1):
                which = self.disc_prometheus[0]
            elif(len(self.disc_prometheus) == 0):
                print "Run Discovery First, or Specify an IP"
            else:
                which = self.select(" ".join(self.disc_prometheus),"Which one?")
        else:
            which = IP(line)

        if(which is not None):
            create_connection(which)


    def do_go(self, line):
        cmdline = line.split(' ')
        if(line == ""):
            message = pm_proto_pb2.pmproto()
            message.type = pm_proto_pb2.pmproto.GO
            message.go = True;
            msg = message.SerializeToString()
            msg = transact_message(msg)
            if(msg is not None):
                message.ParseFromString(msg)
                if message.type == pm_proto_pb2.pmproto.ACK:
                    print "ACK"
                else:
                    print "NAK"
        else:
            message = pm_proto_pb2.pmproto()
            message.type = pm_proto_pb2.pmproto.GO
            message.go = True;
            message.cuestack = int(cmdline[0])
            msg = message.SerializeToString()
            msg = transact_message(msg)
            if(msg is not None):
                message.ParseFromString(msg)
                if message.type == pm_proto_pb2.pmproto.ACK:
                    print "ACK"
                else:
                    print "NAK"


    def do_list(self, line):
        cmdline = line.split(' ')
        if(line == ""):
            cols = int(int(tty_columns) / 7)
            max_fix = max(fix_patch)
            if(cols >= 20):
                for f in xrange(1,max_fix,20):
                    print_fix_line(f,f+20)
            else:
                for f in xrange(1,max_fix,10):
                    print_fix_line(f,f+10)

        elif(cmdline[0] == "patch"):
            print "Listing Patch:"
            print fix_patch
            for key in fix_patch:
                print str(key) + ": " + str(fix_patch[key])

        elif(cmdline[0] == "palette"):
            print "Listing Palettes:"
            for key in colors:
                print str(key) + ": " + str(colors[key])

        elif(cmdline[0] == 'q'):
            print "Listing Cuestack:"
            for key in cue_stacks:
                print str(key) + ": " + str(cue_stacks[key])

        print "List " + line

    def do_load(self, line):
        print "Load " + line

    def do_orecord(self, line):
        print "Only Record " + line

    def do_oupdate(self, line):
        print "Only Update " + line

    def do_oupdate(self, line):
        print "Only Update " + line

    def do_palette(self, line):
        """
        palette 255,255,255 as white

        Store an RGB value as a named color

        palette 11.65,6.634,12.72 as potato

        Store an XYZ color as named color

        palette 3700 as nice_white

        store a color temperature as a named color

        [pal]ette spec as name

        """
        cmdline = line.split(' ')
        argc = len(cmdline)
        if(argc == 3):
            colorslices = cmdline[0].split(',')
            if(len(colorslices) == 1):   # Then we have a color temperature
                colors[str(cmdline[2]).lower()] = {'ct' : int(colorslices[0])}
            elif(len(colorslices) == 3):
                if(is_float(colorslices[0])):  # We have XYZ coordinates
                    colors[str(cmdline[2]).lower()] = {'xyz' : (float(colorslices[0]),float(colorslices[1]),float(colorslices[2]))}
                else:
                    colors[str(cmdline[2]).lower()] = {'rgb' : (int(colorslices[0]),int(colorslices[1]),int(colorslices[2]))}
            else:
                print "Uhh, wtf mate?"

        print "Palette " + line

    def do_patch(self, line):
        """
        [pat]ch fixture @ position as type
                   0    1     2     3  4
        patch 1-3 @ 1 as RGB
        """
        cmdline = line.split(' ')
        argc = len(cmdline)
        fix_list = parseIntSet(cmdline[0])
        has_at = False
        has_as = False
        if(argc == 5):
            if(cmdline[3].lower() == 'as'):
                has_as = True
                fix_type = cmdline[4].lower()
            elif(cmdline[1].lower() == 'as'):
                has_as = True
                fix_type = cmdline[2].lower()
            if(cmdline[1] == '@'):
                has_at = True
                fix_at = int(cmdline[2])
            elif(cmdline[3] == '@'):
                has_at = True
                fix_at = int(cmdline[4])

        elif(argc == 3):
            if(cmdline[1].lower() == 'as'):
                has_as = True
                fix_type = cmdline[2].lower()
            if(cmdline[1] == '@'):
                has_at = True
                fix_at = int(cmdline[2])

        if(argc == 5 and has_as and has_at):
            address_ptr = fix_at
            for fix in fix_list:
                this_fix_type = fixture_types[fix_type]
                #print this_fix_type
                fixture_type = this_fix_type['type']
                fix_label = this_fix_type['label']
                fix_nc = this_fix_type['num_channels']
                fix_int = this_fix_type['intensity']
                fix_vw = this_fix_type['vw']
                fix_rgb = this_fix_type['rgb']
                fix_cm = this_fix_type['channel_map']
                fix_patch[fix] = Patch(fixture_type,address_ptr)
                fix_patch[fix].label = fix_label
                fix_patch[fix].num_channels = fix_nc
                fix_patch[fix].intensity = fix_int
                fix_patch[fix].vw = fix_vw
                fix_patch[fix].rgb = fix_rgb
                fix_patch[fix].channel_map = fix_cm
                address_ptr += fix_nc
                print fix_patch[fix]

        #print "Patch " + line

    def do_record(self, line):
        """record q # t [timespec]

        # is a dotted pair of cue.cuestep

        timespec is comma separated decimal seconds

        wait_time , fade_time

        """
        global current_cue
        cmdline = line.split(' ')
        argc = len(cmdline)
        has_t = False
        has_q = False
        t_spec = (0,0)
        if(argc == 4):
            if(cmdline[0] == 'q'):
                qnum = cmdline[1]
                has_q = True
            elif(cmdline[2] == 'q'):
                qnum = cmdline[3]
                has_q = True
            if(cmdline[0] == 't'):
                tspec = cmdline[1]
                has_t = True
            elif(cmdline[2] == 't'):
                tspec = cmdline[3]
                has_t = True
        elif(argc == 2):
            if(cmdline[0] == 'q'):
                qnum = cmdline[1]
                has_q = True
            if(cmdline[0] == 't'):
                tspec = cmdline[1]
                has_t = True
        if(has_q):
            real_q = qnum.split('.')
            current_cue = (real_q[0],real_q[1])
        if(has_t):
            real_tspec = tspec.split(',')
            tspec = (int(float(real_tspec[0])*1000),int(float(real_tspec[1])*1000))

        record_a_cue(current_cue,tspec,0)

        self.prompt = 'Q' + str(current_cue[0]) + '.' + str(current_cue[1]) + ': '

        print "Record " + line

    def do_release(self, line):
        fix_list = parseIntSet(line)

        for fix in fix_list:
            fix_patch[fix].captured = False
        print "Release " + line

    def do_fixture(self, line):
        """
        [s]et fixture spec [@ color] [i intensity]
                0           1  2      3   4
        """
        cmdline = line.split(' ')
        argc = len(cmdline)
        has_i = False
        has_at = False
        fix_list = parseIntSet(cmdline[0])
        if(argc == 5):
            if(cmdline[3].lower() == 'i'):
                has_i = True
                intensity = cmdline[4]
            elif(cmdline[1].lower() == 'i'):
                has_i = True
                intensity = cmdline[2]
            if(cmdline[1] == '@'):
                has_at = True
                fix_at = cmdline[2]
            elif(cmdline[3] == '@'):
                has_at = True
                fix_at = cmdline[4]
        if(argc == 3):
            if(cmdline[1].lower() == 'as'):
                has_i = True
                intensity = cmdline[2]
            elif(cmdline[1] == '@'):
                has_at = True
                fix_at = cmdline[2]

        for fix in fix_list:
            message = pm_proto_pb2.pmproto()
            message.type = pm_proto_pb2.pmproto.FIXTURE
            message.fixture_id = int(fix)
            fix_patch[fix].captured = True
            if(has_i):
                fix_patch[fix].intensity = parse_intensity(intensity)
                message.intensity = parse_intensity(intensity)
            if(has_at):
                fix_patch[fix].cRGB = parse_color(fix_at,0)
                message.colorspec = parse_color(fix_at,0)
            msg = message.SerializeToString()
            msg = transact_message(msg)
            if(msg is not None):
                message.ParseFromString(msg)
                if message.type == pm_proto_pb2.pmproto.ACK:
                    print "ACK"
                else:
                    print "NAK"

        print "Set " + line

    def do_loadcue(self, line):
        cmdline = line.split(' ')
        argc = len(cmdline)
        if(argc < 2):
            message = pm_proto_pb2.pmproto()
            message.type = pm_proto_pb2.pmproto.LOAD
            message.go = False;
            message.cuestack = 0
            msg = message.SerializeToString()
            msg = transact_message(msg)
            if(msg is not None):
                message.ParseFromString(msg)
                if message.type == pm_proto_pb2.pmproto.ACK:
                    print "ACK"
                else:
                    print "NAK"
        elif(argc == 2):
            message = pm_proto_pb2.pmproto()
            message.type = pm_proto_pb2.pmproto.LOAD
            message.go = False;
            message.cuestack = int(cmdline[0])
            message.fixture_id = int(cmdline[1])
            msg = message.SerializeToString()
            msg = transact_message(msg)
            if(msg is not None):
                message.ParseFromString(msg)
                if message.type == pm_proto_pb2.pmproto.ACK:
                    print "ACK"
                else:
                    print "NAK"
        print "Load Cue " + line

    def do_loadandgo(self, line):
        cmdline = line.split(' ')
        argc = len(cmdline)
        if(argc < 2):
            message = pm_proto_pb2.pmproto()
            message.type = pm_proto_pb2.pmproto.LOAD
            message.go = True;
            message.cuestack = 0
            msg = message.SerializeToString()
            msg = transact_message(msg)
            if(msg is not None):
                message.ParseFromString(msg)
                if message.type == pm_proto_pb2.pmproto.ACK:
                    print "ACK"
                else:
                    print "NAK"
        elif(argc == 2):
            message = pm_proto_pb2.pmproto()
            message.type = pm_proto_pb2.pmproto.LOAD
            message.go = True;
            message.cuestack = int(cmdline[0])
            message.fixture_id = int(cmdline[1])
            msg = message.SerializeToString()
            msg = transact_message(msg)
            if(msg is not None):
                message.ParseFromString(msg)
                if message.type == pm_proto_pb2.pmproto.ACK:
                    print "ACK"
                else:
                    print "NAK"
        print "Load and Go Cue " + line


    def do_unpatch(self, line):
        print "Unpatch " + line

    def do_update(self, line):
        print "Update " + line

    def do_EOF(self, line):
        return True

"""
message fixture {
  required uint32 fixture_id = 1;
  optional string label = 2 [(nanopb).max_size = 20];
  required uint32 fixture_type = 3;
  required uint32 start_address = 4;
  optional bool intensity = 10;
  optional bool rgb = 11;
  optional bool vw = 12;
  optional uint32 num_channels = 20;
  optional bytes channel_map = 21 [(nanopb).max_size = 32];
  optional uint32 vw_cool = 30;
  optional uint32 vw_warm = 31;
}
typedef struct _fixture_fader {
  char label[20];
  uint16_t fixture_type;
  uint16_t start_address;
  uint8_t num_channels;
  bool intensity;
  bool rgb;
  bool vw;
  uint16_t vw_cool; // Cool CT
  uint16_t vw_warm; // Warm CT
  uint32_t cVW_t; // CT target
  uint32_t cVW_s; // CT inital
  uint32_t cVW; // CT current
  uint64_t cVW_start; // CT start time
  uint64_t cVW_time; // CT target time
  uint32_t cRGB; // 8-bit RGB current
  uint32_t cRGB_t; // 8-bit RGB target
  uint32_t cRGB_s; // 8-bit RGB start
  uint64_t cRGB_start; // RGB start time
  uint64_t cRGB_time; // RGB target time
  uint16_t level; // Overall level current from 0-65k
  uint16_t level_t; // Level target
  uint16_t level_s; // Level start
  uint64_t level_start; // Level start time
  uint64_t level_time; // Level target time
  uint8_t channel_map[32]; // Channel map

  #ifdef USE_XYZ
  cXYZ cXYZ_t;
  cXYZ cXYZ_s;
  #endif

  #ifdef USE_LAB
  cLAB cLAB_t;
  cLAB cLAB_s;
  #endif USE_LAB

} fixture_fader;
"""

class Patch(object):
    label = ""
    fixture_type = 0
    start_address = 0
    intensity = False
    rgb = False
    vw = False
    num_channels = 0
    channel_map = []
    vw_cool = 0
    vw_warm = 0
    cVW = 0
    cRGB = 0
    cXYZ = 0
    level = 0

    captured = False

    def __init__(self,fixture_type,start_address):
        self.fixture_type = fixture_type
        self.start_address = start_address

    def __str__(self):
        return self.label + ": " + str(self.fixture_type) + "/" + str(self.start_address) + " [" + str(self.num_channels) + "]"


cue_stacks = {}

class Cuestack(object):
    label = ""
    cuestack_id = ""
    tweet = ""
    num_cuesteps = 0
    loop = False
    current_step = 0

    cuesteps = {}

    def __str__(self):
        retstr = ""
        for step in self.cuesteps:
            retstr += "Cuestep: " + str(step) + "\n"
            retstr += str(self.cuesteps[step])
            retstr += "====="
        return retstr

    def __init__(self, cuestack_id, num_cuesteps):
        self.cuestack_id = cuestack_id
        self.num_cuesteps = num_cuesteps


class CueStep(object):
    label = ""
    wait_time = 0
    fix_count = 0

    cue_fix = []

    def __str__(self):
        retstr = "Wait: " + str(self.wait_time) + "\n"
        retstr += "Fix_count: " + str(self.fix_count) + "\n"
        for step in self.cue_fix:
            retstr += str(step)
        return retstr

    def __init__(self, wait_time, fix_count):
        self.wait_time = wait_time
        self.fix_count = fix_count

class CueFix(object):

    crgb = None
    cvw = None
    white = None
    intensity = None

    fixture_id = 0

    fade_time = 0

    def __str__(self):
        retstr = "Fix: " + str(self.fixture_id) + " Fade: " + str(self.fade_time) + "\n"
        if(self.intensity is not None):
            retstr += "Int: " + str(self.intensity) + "\n"
        if(self.crgb is not None):
            retstr += "Color: " + str(self.crgb) + "\n"
        return retstr

    def __init__(self, fixture_id, fade_time):
        self.fixture_id = fixture_id
        self.fade_time = fade_time

tty_rows, tty_columns = os.popen('stty size', 'r').read().split()

fix_patch = {}

if __name__ == '__main__':
    global prometheus_ip
    prometheus_ip = None
    app = App()
    app.cmdloop()
