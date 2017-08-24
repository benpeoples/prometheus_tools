# Prometheus Cue JSON

Approximate format:

    {
      "version" : integer,
      "cuestacks" : [
      {
        "cuestack_id" : integer (required),
        "label" : string (max 20 chars),
        "tweet" : string (max 140 chars),
        "loop" : bool,
        "cuesteps" : [
          {
            "wait" : integer (required) - number of milliseconds to wait before stepping,
            "fixtures" : [
            {
              "fixture_id" : integer,
              "color" : {
                "red" : integer,
                "green" : integer,
                "blue" : integer,
                "white" : integer,
                "warm" : integer,
                "cool" : integer,
                "intensity" : integer (0-65535)
              },
              "fade" : integer (milliseconds to fade this cuefix in)
            },
            (more fixtures)
            ]
          },
          (more cuesteps)
        ]
      },
      (more cuestacks)
    }

## Notes on timing

`wait` determines how long the cuestep should wait before executing the next cuestep, while `fade` determines individual fixture fades.    

If you do not specify a `fade`, `json_to_stack` will apply `wait` to every fixture in the cuestep.   `stack_to_json` will not strip `fade` from the file, so you will get a `fade` on every fixture when you extract it.  

Only the properties contained in a given cuefix (the "fixtures" array) are affected.  If you change `intensity`, it will not affect color, even if ongoing fades are happening.

There's a corner case where you only specify one or two of red, green, or blue.  The fader logic takes the previous *target* for the missing value.   This prevents you from ending up in an unknown color state.

# patch_upload.py

    stack_upload.py ip_address stack.bin

Stack upload is pretty dumb at the moment, and is just streamed over TCP.   We will be adding a checksum function soonish.  

Process is pretty simple, connect to TCP port 1234 send the four byte password followed by `0x02` for a stack file.  Then send four bytes of filesize in octets-- this is primarily used to clear enough flash space for the file. Then just stream the file.   Before the file we're going to add an md5 checksum, but currently not there.

We will probably need to add a "ready" command from the controller to the software-- a large patch file will take a long time to clear the flash space, additionally we will not have enough buffer space on the device for a full patch file if it is streamed too fast.  

There is a 30 second timeout on TCP data, so if you are having trouble, you may want to add some sleeps between packets.  
