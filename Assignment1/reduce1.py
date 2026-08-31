
import sys

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
