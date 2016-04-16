#!/bin/bash

export PID_FILE='.crowbar-demo.pid'
export PID_PREV="$(cat $PID_FILE)"

if [[ "$(cat /proc/$PID_PREV/comm)" == 'crowbar-demo' ]]; then
    kill -2 $PID_PREV
fi

./demo &
pid=$!
echo "$pid" > $PID_FILE
wait $pid
