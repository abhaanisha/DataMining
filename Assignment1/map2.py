

import sys


try:
    import signal
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except (ImportError, AttributeError, ValueError):
    pass

TOTAL_KEY = "0" * 13       

for line in sys.stdin:
    line = line.rstrip("\n")
    if not line.strip():
        continue
    key, count, _values = line.split("\t", 2)
    print("%s\t%s" % (TOTAL_KEY, count))
    print(line)
