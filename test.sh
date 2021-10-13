mkdir logs 2>/dev/null || true
IP1=192.168.0.1
IP2=100.1.0.9
MAC=00:90:fb:62:c4:96 
nice -20 python3 -u peer.py recv eth16 $MAC $IP2 $IP1 > logs/test-${1}-recv.log &
nice -20 python3 -u peer.py send eth0 $MAC $IP2 $IP1 &
#tail -F logs/test-${1}-recv.log | python3 -u gaps.py 0.1
tail -F logs/test-${1}-recv.log
JOBS=$(jobs -p)
kill -2 $JOBS
wait
