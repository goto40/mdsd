# Wireshark Demo

## UDP

`run_tests.sh' does the following;

 * generates python code (for the data sender scripts [send_via_udp.py](scripts/send_via_udp.py) and [send_via_udp2.py](scripts/send_via_udp2.py))
 * generates lua code (for wireshark)
 * starts `tshark`
   * with the generated lua dissectors ([multimessage.dissector](model/multimessage.dissector) and (polygon.dissector)[model/polygon.dissector]: `-X lua_script:src-gen/lua/multimessage.lua -X lua_script:src-gen/lua/polygon.lua`
   * with an UDP port filter: `-Y "udp.port==50000 || udp.port==60000"`
   * and an appropriate output formatting for the dissector layers (key,value): `-T ek -J "multimessage polygon"`
 * send some data ("`SENDING DATA`")
 * kill tshark ("`KILLING TSHARK`")

Output:
```
...
SENDING DATA:
send 0: 296 bytes...
send 1: 20 bytes...
send 2: 72 bytes...
send 0: 284 bytes...
send 1: 292 bytes...
send 2: 300 bytes...
{"index":{"_index":"packets-2021-07-17","_type":"doc"}}
{"timestamp":"1626523675552","layers":{"frame":{"filtered":"frame"},"eth":{"filtered":"eth"},"ip":{"filtered":"ip"},"udp":{"filtered":"udp"},"_ws_lua__ws_lua_fake":{"filtered
":"_ws.lua.fake"},"multimessage":{"multimessage":[{"multimessage_id":"2","multimessage_length":"296"},{"multimessage_n":"3","multimessage":[{"multimessage":[{"multimessage_x"
:"0.99","multimessage_y":"-0.33"},{"multimessage_x":"1.99","multimessage_y":"-1.33"},{"multimessage_x":"2.99","multimessage_y":"-2.33"}]},{"multimessage_info":["121","111","1
17","114","32","102","97","118","111","114","105","116","101","32","112","111","108","121","103","111","110","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","
0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"
,"0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","
0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"
,"0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","
0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"
,"0"]}]}],"multimessage_mycontainer":"4294564291","multimessage_code":"-99","multimessage___onoff_0":"1","multimessage___onoff_1":"0","multimessage___onoff_2":"0","multimessa
ge___onoff_3":"1","multimessage___onoff_4":"1","multimessage___onoff_5":"1","multimessage___onoff_6":"0","multimessage___onoff_7":"0","multimessage___onoff_8":"0","multimessa
ge___onoff_9":"0","multimessage_abc":"-1"}}}
{"index":{"_index":"packets-2021-07-17","_type":"doc"}}
{"timestamp":"1626523675552","layers":{"frame":{"filtered":"frame"},"eth":{"filtered":"eth"},"ip":{"filtered":"ip"},"udp":{"filtered":"udp"},"_ws_lua__ws_lua_fake":{"filtered
":"_ws.lua.fake"},"multimessage":{"multimessage":[{"multimessage_id":"1","multimessage_length":"20"},{"multimessage_x":"1","multimessage_y":"2"}],"multimessage_mycontainer":"
413696","multimessage_code":"101","multimessage___onoff_0":"0","multimessage___onoff_1":"0","multimessage___onoff_2":"0","multimessage___onoff_3":"0","multimessage___onoff_4"
:"0","multimessage___onoff_5":"0","multimessage___onoff_6":"0","multimessage___onoff_7":"0","multimessage___onoff_8":"0","multimessage___onoff_9":"0","multimessage_abc":"0"}}
}
{"index":{"_index":"packets-2021-07-17","_type":"doc"}}
{"timestamp":"1626523675553","layers":{"frame":{"filtered":"frame"},"eth":{"filtered":"eth"},"ip":{"filtered":"ip"},"udp":{"filtered":"udp"},"_ws_lua__ws_lua_fake":{"filtered
":"_ws.lua.fake"},"multimessage":{"multimessage":[{"multimessage_id":"3","multimessage_length":"72"},{"multimessage":[{"multimessage":[{"multimessage_x":"0","multimessage_y":
"0"},{"multimessage_x":"0","multimessage_y":"0"},{"multimessage_x":"0","multimessage_y":"0"}]},{"multimessage":[{"multimessage":{"multimessage_rgb":["0","0","0"]}},{"multimes
sage":{"multimessage_rgb":["0","0","0"]}},{"multimessage":{"multimessage_rgb":["0","0","0"]}}]}]}],"multimessage_mycontainer":"417792","multimessage_code":"102","multimessage
___onoff_0":"0","multimessage___onoff_1":"0","multimessage___onoff_2":"0","multimessage___onoff_3":"0","multimessage___onoff_4":"0","multimessage___onoff_5":"0","multimessage
___onoff_6":"0","multimessage___onoff_7":"0","multimessage___onoff_8":"0","multimessage___onoff_9":"0","multimessage_abc":"0"}}}
{"index":{"_index":"packets-2021-07-17","_type":"doc"}}
{"timestamp":"1626523675738","layers":{"frame":{"filtered":"frame"},"eth":{"filtered":"eth"},"ip":{"filtered":"ip"},"udp":{"filtered":"udp"},"_ws_lua__ws_lua_fake":{"filtered":"_ws.lua.fake"},"polygon":{"polygon_n":"3","polygon":[{"polygon":[{"polygon_x":"0.99","polygon_y":"-0.33"},{"polygon_x":"1.99","polygon_y":"-1.33"},{"polygon_x":"2.99","polygon_y":"-2.33"}]},{"polygon_info":["121","111","117","114","32","102","97","118","111","114","105","116","101","32","112","111","108","121","103","111","110","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]}]}}}
{"index":{"_index":"packets-2021-07-17","_type":"doc"}}
{"timestamp":"1626523675738","layers":{"frame":{"filtered":"frame"},"eth":{"filtered":"eth"},"ip":{"filtered":"ip"},"udp":{"filtered":"udp"},"_ws_lua__ws_lua_fake":{"filtered":"_ws.lua.fake"},"polygon":{"polygon_n":"4","polygon":[{"polygon":[{"polygon_x":"0.99","polygon_y":"-0.33"},{"polygon_x":"1.99","polygon_y":"-1.33"},{"polygon_x":"2.99","polygon_y":"-2.33"},{"polygon_x":"3.99","polygon_y":"-3.33"}]},{"polygon_info":["121","111","117","114","32","102","97","118","111","114","105","116","101","32","112","111","108","121","103","111","110","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]}]}}}
{"index":{"_index":"packets-2021-07-17","_type":"doc"}}
{"timestamp":"1626523675738","layers":{"frame":{"filtered":"frame"},"eth":{"filtered":"eth"},"ip":{"filtered":"ip"},"udp":{"filtered":"udp"},"_ws_lua__ws_lua_fake":{"filtered":"_ws.lua.fake"},"polygon":{"polygon_n":"5","polygon":[{"polygon":[{"polygon_x":"0.99","polygon_y":"-0.33"},{"polygon_x":"1.99","polygon_y":"-1.33"},{"polygon_x":"2.99","polygon_y":"-2.33"},{"polygon_x":"3.99","polygon_y":"-3.33"},{"polygon_x":"4.99","polygon_y":"-4.33"}]},{"polygon_info":["121","111","117","114","32","102","97","118","111","114","105","116","101","32","112","111","108","121","103","111","110","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]}]}}}
KILLING TSHARK...
```