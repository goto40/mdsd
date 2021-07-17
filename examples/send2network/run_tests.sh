#!/bin/bash

./generate_python.sh
./generate_lua.sh

{
    sleep 2
    echo "SENDING DATA:"
    ./send_data.sh
} &

sudo -- bash -c 'tshark -X lua_script:src-gen/lua/multimessage.lua -X lua_script:src-gen/lua/polygon.lua -Y "udp.port==50000 || udp.port==60000" -T ek -J "multimessage polygon" & PID=$! && echo "TSHARK READY @ $PID" && sleep 5 && echo "KILLING TSHARK..." && kill $PID'


