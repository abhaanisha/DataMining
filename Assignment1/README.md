# MapReduce Median

Computes the exact median of `median.txt` (one number per line) using two
MapReduce rounds joined by `sort`.

## Run

```bash
cat median.txt | python3 map1.py | sort | python3 reduce1.py | python3 map2.py | sort | python3 reduce2.py
```

Output:

```
median	495.5559479
```

Works with `python` too if that is Python 3 on your machine. No third-party
packages are needed.

## Files

| File       | Role                                                                  |
|------------|-----------------------------------------------------------------------|
| map1.py    | Bins each value; emits `1<bucket>` -> `<value>`                        |
| reduce1.py | Collapses a bucket to `1<bucket>` -> `<count>`, `<sorted values>`      |
| map2.py    | Emits each bucket's size to one global key; passes the bucket through  |
| reduce2.py | Sums the counts into n, then finds the value(s) at the median rank     |

Keys are fixed-width digit strings, so a plain `sort` (no `-n`, no `LC_ALL=C`)
groups and orders them correctly.

## Inspecting a stage

Stop the pipeline anywhere to see the intermediate records:

```bash
cat median.txt | python3 map1.py | sort | python3 reduce1.py | head
```

## Other input

Any file with one number per line works:

```bash
printf '3\n1\n5\n2\n4\n' | python3 map1.py | sort | python3 reduce1.py | python3 map2.py | sort | python3 reduce2.py
# median	3.0
```
