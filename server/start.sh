#!/bin/bash

cd `dirname $0`
python_ver=$(ls /usr/bin|grep -e "^python[3]\.[1-9]\+$"|tail -1)
eval $(ps -ef | grep "[0-9] ${python_ver} status_monitor_server\\.py" | awk '{print "kill "$2}')
nohup ${python_ver} status_monitor_server.py >> server.log 2>&1 &
if [[ $? = 0 ]]; then
    echo "启动完毕"
fi
