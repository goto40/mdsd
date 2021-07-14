#!/bin/bash

textx generate model/*.item --overwrite --target lua_dissector --output-path src-gen/lua || exit 1
textx generate model/*.dissector --overwrite --target lua_dissector --output-path src-gen/lua || exit 1

