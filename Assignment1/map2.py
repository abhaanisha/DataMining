#!/usr/bin/env python3
"""
Round 2 mapper -- send every bucket's size to one global key, pass the bucket on.

  in  : <bucket key> \t <count> \t <values>
  out : 0000000000000 \t <count>                   partial global count
        <bucket key>  \t <count> \t <values>       the bucket, unchanged

Tag "0" sorts before every bucket's tag "1", so `sort` hands reduce2.py all of
the partial counts first.  That is what lets the reducer know n before it sees
a single bucket, and therefore find the median in one streaming pass.
"""

import sys

# behave like a normal unix filter when the downstream stage stops reading (e.g. `| head`)
try:
    import signal
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except (ImportError, AttributeError, ValueError):
    pass

TOTAL_KEY = "0" * 13        # same width as a bucket key, sorts ahead of all of them

for line in sys.stdin:
    line = line.rstrip("\n")
    if not line.strip():
        continue
    key, count, _values = line.split("\t", 2)
    print("%s\t%s" % (TOTAL_KEY, count))
    print(line)
