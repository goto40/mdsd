-- https://mika-s.github.io/wireshark/lua/dissector/2017/11/04/creating-a-wireshark-dissector-in-lua-1.html
-- sudo wireshark -X lua_script:manual.lua 
-- reload: ctrl-shift-L

manual_protocol = Proto("MyManualProto",  "My Manual Protocol")

field_n = ProtoField.uint32("mymanual.n", "n", base.DEC)

manual_protocol.fields = { field_n }

function manual_protocol.dissector(buffer, pinfo, tree)
  length = buffer:len()
  if length == 0 then return end

  pinfo.cols.protocol = manual_protocol.name

  local subtree = tree:add(manual_protocol, buffer(), "MyMannualProto Data")

  subtree:add_le(field_n, buffer(0,4))
end

local udp_port = DissectorTable.get("udp.port")
udp_port:add(50000, manual_protocol)
