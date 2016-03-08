#!/bin/bash
SECONDS=0
elapsed=${2:-600}
last=$(gdb -batch -ex "attach $1"  -ex "bt" 2>&1 -ex "detach" \
        | grep -v ^"No stack."$ | md5sum)
while [ $SECONDS -lt $elapsed ]; do
    sleep 5;
    current=$(gdb -batch -ex "attach $1"  -ex "bt" 2>&1 -ex "detach" \
                | grep -v ^"No stack."$ | md5sum)
    if [ "$current" != "$last" ]; then
        echo "PROCESS NOT STUCK!";
        return;
    fi
    last=$current
done
echo "PROCESS STUCK!"