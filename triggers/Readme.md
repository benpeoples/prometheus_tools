# Prometheus Trigger JSON

Approximate format:

    [  {
        "trigger_id" : 32-bit integer (required),
        "start_month" : 1-12 (optional, can wrap),
        "start_day" : 1-31 (optional),
        "end_month" : 1-12 (optional, can wrap),
        "end_day" : 1-31 (opt),
        "day_of_week" : [false,true,true,true,true,true,false], (day of week mask, Sunday start)
        "start_type" : 0 (see protobuf),
        "start" : 28800 (offset in seconds),
        "end_type" : 2 (see protobuf),
        "end" : -1800 (offset in seconds),
        "priority" : 100,
        "action" : "c|1|t|0|1|2|t|1500|2|" action string
      },
      (more triggers)
    ]

I think we need to add a start_type for "manual"... so let's call that 6 and I'll update the protobuf.

## Trigger sources

Start Date - month | day
End Date - month | day

- Day of week mask: 0SFRWTMS

- Start ENUM:

0 = TIME

1 = SUNRISE

2 = SUNSET

3 = NOON

4 = MIDNIGHT

5 = RANDOM

6 = MANUAL

- Start Hour (or offset) - seconds (since midnight)
- End ENUM:

0 = TIME

1 = SUNRISE

2 = SUNSET

3 = NOON

4 = MIDNIGHT

5 = RANDOM

6 = MANUAL

- End Hour (or offset) - seconds (since midnight)

Random will pick a random start time < end time.

Not specifying a start or end date will wildcard match.
Not specifying a start or end time or type will wildcard match all.

Priority is a 32-bit unsigned int, higher priority triggers will suppress lower priority triggers.  I think this means you set your "everyday" priority, then set holidays at higher priorities.


## Action is a string defining what to do

### Actions:

- Send OSC message (o)
- Send UDP message (u)
- Cuestack action (c)
- triggers (t)

### Action format:

    <message type><params><content>

OSC/UDP message parameters:
|ip_address|port|

    u|192.168.1.1|9000|23|themessagegoeshereuntilNULL

    o|192.168.1.1|54000|13|rawoscmessage

Cuestack action:

‘c’ -- clear
‘l’ -- load
‘t’ -- load and go
‘g’ -- go
‘x’ -- stop

    c|id|action|milliseconds|fader|

can repeat cuestacks:

    c|id|action|milliseconds|fader|id|action|milliseconds|fader|

So:

    c|1|t|0|1|

Load-and-go cuestack 1 on fader 1

or

    c|1|t|0|1|2|t|1500|2|

Load-and-go cuestack 1 on fader 1, cuestack 2 on fader 2 with a 1500ms delay

Like with the lan protocol, cuestack 0 means go black

Triggers:

    t|id|milliseconds|

Can repeat triggers:

    t|id|milliseconds|id|milliseconds|

so:

    t|1|0|2|50000|

Trigger 1 with 0 milliseconds delay, then 50 seconds later trigger 2

- You cannot trigger yourself with < 1 second delay
- Trigger triggers are why I think we need a manual option.
