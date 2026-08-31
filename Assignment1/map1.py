
import math
import sys

try:
    import signal
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except (ImportError, AttributeError, ValueError):
    pass

BIN_WIDTH = 1.0             
WIDTH = 12                  
OFFSET = 10 ** 11           


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
