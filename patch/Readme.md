# Prometheus Patch JSON

Approximate Format:

    [
      {
        "fixture_id" : integer (required),
        "label" : string (truncated to 20 chars),
        "fixture_type" : integer (required),
        "start_address" : integer (1 = Universe A, 513 = Universe B) (required),
        "num_channels" : integer,
        "channel_map" : array of integers,
        "vw_cool" : integer (color temp in K of cool white)
        "vw_warm" : integer (color temp in K of warm white)
      },
      etc.
    ]

### Channel map
Channel map is an array of up to 32 bytes that indicate that fixture's patch layout -- array of integers

Channel map values:

- 0x00 : Not used
- 0x01 : Intensity
- 0x02 : Red
- 0x03 : Green
- 0x04 : Blue
- 0x05 : White
- 0x06 : Cool White
- 0x07 : Warm White

## fixture_id

Arbitrary number to identify the fixture, does not need to be continuous, but cannot be duplicated.

## fixture_type

Arbitrary number to identify all of the same kind of fixture, no real purpose in the system right now.

# JSON TO PATCH

    json_to_patch.py patch.json patch.bin

Will create or overwrite `patch.bin` with a new patch file.  Will spit out errors and return -1 if your json has problems, will currently just throw a random exception if your json is malformed.

# PATCH TO JSON

    patch_to_json.py patch.bin patch.json

Will create or overwrite `patch.json` with a new json patch.   Will spit out errors if `patch.bin` is not formatted like a patch file.  

# patch_upload.py

    patch_upload.py ip_address patch.bin

Patch upload is pretty dumb at the moment, and is just streamed over TCP.   We will be adding a checksum function soonish.  

Process is pretty simple, connect to TCP port 1234 send the four byte password followed by `0x01` for a patch file.   The just stream the file.   Before the file we're going to add an md5 checksum, but currently not there.
