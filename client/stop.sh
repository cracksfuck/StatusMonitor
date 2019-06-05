#!/bin/bash

python_ver=$(ls /usr/bin|grep -e "^python[3]\.[1-9]\+$"|tail -1)
eval $(ps -ef | grep "[0-9] ${python_ver} status_monitor_client\\.py" | awk '{print "kill "$2}')
echo "停止完毕"
