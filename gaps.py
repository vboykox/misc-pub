import sys

_, interval, *_ = sys.argv + ['0.001'] 
interval = float(interval)

prev_ts = None
while True:
    l = sys.stdin.readline()
    if not l: break
    ts, idx = l.split(':')
    ts = float(ts)
    idx = int(idx)
    if prev_ts is not None:
        diff = abs(ts - prev_ts)
        if diff > interval:
            diff_idx = idx - prev_idx 
            print(diff_idx, diff, prev_ts, prev_idx, ts, idx)
    prev_ts = ts
    prev_idx = idx
