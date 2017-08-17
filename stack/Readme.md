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

`wait` determines how long the cuestep should wait before executing the next cuestep, while `fade` determines individual fixture fades.    I think it is reasonable to expect that if you do not specify fade that fade == wait.   Only the properties contained in a given cuefix (the "fixtures" array) are affected.  If you change `intensity`, it will not affect color, even if ongoing fades are happening.