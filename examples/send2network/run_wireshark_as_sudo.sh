#!/bin/bash

./generate_lua.sh

echo "SHIFT-CTRL-L == reload scripts"
echo "use filter: udp.port==50000 || udp.port==50000"
#sudo wireshark -X lua_script:src-gen/lua/multimessage.lua -Y "udp.port==50000 || udp.port==60000"
sudo wireshark -X lua_script:src-gen/lua/multimessage.lua -X lua_script:src-gen/lua/polygon.lua -Y "udp.port==50000 || udp.port==60000"

