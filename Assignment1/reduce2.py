
import sys


try:
    import signal
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except (ImportError, AttributeError, ValueError):
    pass

TOTAL_KEY = "0" * 13

n = 0
ranks = None                
picked = []
seen = 0                    

for line in sys.stdin:
    line = line.rstrip("\n")
    if not line.strip():
        continue
    parts = line.split("\t")

    if parts[0] == TOTAL_KEY:
        n += int(parts[1])
        continue

    if ranks is None:                       
        if n == 0:
            sys.exit("no values in the input")
        ranks = [(n + 1) // 2] if n % 2 else [n // 2, n // 2 + 1]

    count = int(parts[1])
    low, high = seen + 1, seen + count     
    seen = high

    if len(picked) == len(ranks):          
        continue

    wanted = [r for r in ranks if low <= r <= high]
    if wanted:
        values = [float(x) for x in parts[2].split(",")]
        for r in wanted:
            picked.append(values[r - low])

if ranks is None or len(picked) != len(ranks):
    sys.exit("could not determine the median")

print("median\t%r" % (sum(picked) / len(picked)))
