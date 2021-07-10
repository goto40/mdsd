#!/bin/bash
echo "SHIFT-CTRL-L == reload scripts"
echo "use filter: udp.port==50000"
sudo wireshark -X lua_script:manual/manual.lua

