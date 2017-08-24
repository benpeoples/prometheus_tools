# Cmdline Programmer

Uses the pm_proto protocol to talk to the device.

## Commands that work:

- find (finds devices on the network)
- connect IP_ADDRESS
- ping (make sure device is attached and active)
- palette (palettizes color locally)
- fixture (sets fixtures to values)
- patch (patches fixtures, locally)
- loadcue (loads a cue)
- loadandgo (loads and goes a cue)
- go (runs a cue)

## find

Find sends the string "ping" to port 1557 on 255.255.255.255 and looks for responses.  Mirandas send "pong" back.

## connect

Connect to a specific IP address, sends a PING to make sure it's there.

## ping

Sends a PM_PROTO ping and looks for a PONG

## palette

    palette 255,255,255 as white

Store an RGB value as a named color

## fixture

    fix 1 @ white i 100%

    [fix]ture fixture spec [@ color] [i intensity]

    fix 1-10 @ red i 50%

## patch

    patch 1-10 @ 1 as rgb

Patches 10 rgb fixtures starting at dmx 1

## loadcue

   loadcue a b

loads cue a into playback b (limit of 12 playbacks)

   loadcue 1 2

loads cue 1 into playback 2

   loadcue 0 0 (clears output)

## loadandgo

Just like loadcue, but starts the cuestack immeidately

## go

   go playback#

`go 0` stops all cues and 0's output

   go 1

starts playback 1
