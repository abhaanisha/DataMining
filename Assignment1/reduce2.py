#!/usr/bin/env python3
"""
Round 2 reducer -- pick the median.

  in  : 0000000000000 \t <count>                   all of these arrive first
        <bucket key>  \t <count> \t <values>       buckets, ascending
  out : median \t <value>

n is summed from the leading count records, which fixes the 1-based rank(s) the
median sits at: (n+1)/2 for odd n, n/2 and n/2+1 averaged for even n.  The
buckets then stream past a running cumulative count, and a bucket is unpacked
only when a wanted rank falls inside it -- so at most one bucket's values are
in memory.
"""

import sys

# behave like a normal unix filter when the downstream stage stops reading (e.g. `| head`)
try:
    import signal
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except (ImportError, AttributeError, ValueError):
    pass

TOTAL_KEY = "0" * 13

n = 0
ranks = None                # 1-based ranks that make up the median
picked = []
seen = 0                    # values covered by the buckets read so far

for line in sys.stdin:
    line = line.rstrip("\n")
    if not line.strip():
        continue
    parts = line.split("\t")

    if parts[0] == TOTAL_KEY:
        n += int(parts[1])
        continue

    if ranks is None:                       # first bucket: n is now final
        if n == 0:
            sys.exit("no values in the input")
        ranks = [(n + 1) // 2] if n % 2 else [n // 2, n // 2 + 1]

    count = int(parts[1])
    low, high = seen + 1, seen + count      # ranks this bucket covers
    seen = high

    if len(picked) == len(ranks):           # done, but keep draining stdin
        continue

    wanted = [r for r in ranks if low <= r <= high]
    if wanted:
        values = [float(x) for x in parts[2].split(",")]
        for r in wanted:
            picked.append(values[r - low])

if ranks is None or len(picked) != len(ranks):
    sys.exit("could not determine the median")

print("median\t%r" % (sum(picked) / len(picked)))
