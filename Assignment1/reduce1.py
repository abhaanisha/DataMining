#!/usr/bin/env python3
"""
Round 1 reducer -- collapse one bucket into one record.

  in  : <bucket key> \t <value>                    (grouped by key by `sort`)
  out : <bucket key> \t <count> \t <v1,v2,...>     values ascending

Only the values of the bucket currently being read are held in memory.
"""

import sys

# behave like a normal unix filter when the downstream stage stops reading (e.g. `| head`)
try:
    import signal
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except (ImportError, AttributeError, ValueError):
    pass


def emit(key, values):
    if key is None:
        return
    values.sort()
    print("%s\t%d\t%s" % (key, len(values), ",".join(repr(v) for v in values)))


current = None
values = []

for line in sys.stdin:
    line = line.rstrip("\n")
    if not line.strip():
        continue
    key, value = line.split("\t", 1)
    if key != current:
        emit(current, values)
        current, values = key, []
    values.append(float(value))

emit(current, values)
