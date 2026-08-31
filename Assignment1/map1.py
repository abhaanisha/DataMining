#!/usr/bin/env python3
"""
Round 1 mapper -- bucketise every value.

  in  : one numeric value per line
  out : <bucket key> \t <value>

The bucket key is "1" followed by a fixed-width, zero-padded bucket id
(floor(v / BIN_WIDTH), shifted by OFFSET so negative inputs stay non-negative).
Every key this job ever emits is a digit string of the same length, so the
plain `sort` between mapper and reducer orders keys exactly the way a numeric
sort would, under any locale.  Leading tag "1" is for data buckets; tag "0" is
reserved for the global-count key that map2.py introduces, which is what makes
the count reach reduce2.py ahead of the buckets.
"""

import math
import sys

# behave like a normal unix filter when the downstream stage stops reading (e.g. `| head`)
try:
    import signal
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except (ImportError, AttributeError, ValueError):
    pass

BIN_WIDTH = 1.0             # values that land in the same unit interval group together
WIDTH = 12                  # digits in the padded bucket id
OFFSET = 10 ** 11           # shift so bucket ids are non-negative


def bucket_key(v):
    b = int(math.floor(v / BIN_WIDTH)) + OFFSET
    s = str(b)
    if len(s) > WIDTH:
        sys.exit("value %r out of the supported range" % v)
    return "1" + s.zfill(WIDTH)


for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    for field in line.replace(",", " ").split():
        try:
            v = float(field)
        except ValueError:
            print("skipping non-numeric token %r" % field, file=sys.stderr)
            continue
        print("%s\t%r" % (bucket_key(v), v))
