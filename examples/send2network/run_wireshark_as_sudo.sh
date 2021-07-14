#!/bin/bash

textx generate model/*.item --overwrite --target lua_dissector --output-path src-gen/lua || exit 1
textx generate model/*.dissector --overwrite --target lua_dissector --output-path src-gen/lua || exit 1

echo "SHIFT-CTRL-L == reload scripts"
echo "use filter: udp.port==50000"
sudo wireshark -X lua_script:src-gen/lua/polygon.lua

