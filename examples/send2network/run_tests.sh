#!/bin/bash

textx generate model/*.item --overwrite --target python --output-path src-gen/python || exit 1
textx generate model/*.item --overwrite --target lua_dissector --output-path src-gen/lua || exit 1

./send_data.sh

