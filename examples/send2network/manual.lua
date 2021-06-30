-- https://mika-s.github.io/wireshark/lua/dissector/2017/11/04/creating-a-wireshark-dissector-in-lua-1.html
-- https://mika-s.github.io/topics/
-- sudo wireshark -X lua_script:manual.lua 
-- reload: ctrl-shift-L
-- cool: https://mika-s.github.io/wireshark/lua/dissector/usb/2019/07/23/creating-a-wireshark-usb-dissector-in-lua-1.html
-- https://sharkfestus.wireshark.org/sharkfest.09/DT06_Bjorlykke_Lua%20Scripting%20in%20Wireshark.pdf
-- https://users.informatik.haw-hamburg.de/~schulz/pub/Rechnernetze/tools/wireshark/WiresharkFullDocumentation.pdf


field_x = ProtoField.float("x", "x", base.DEC)
field_y = ProtoField.float("y", "y", base.DEC)

manual_protocol = Proto("MyManualProto",  "My Manual Protocol")
field_n = ProtoField.uint32("mymanual.n", "n", base.DEC)
manual_protocol.fields = { field_n, field_x, field_y }

function manual_protocol.dissector(buffer, pinfo, tree)
  length = buffer:len()
  if length == 0 then return end

  pinfo.cols.protocol = manual_protocol.name

  local subtree = tree:add(manual_protocol, buffer(), "MyMannualProto Data")
  subtree:add_le(field_n, buffer(0,4))

  pos = 0;
  pos0 = pos;
  local subtree_p = subtree:add(manual_protocol, buffer(), "Points p")
  pos = pos + 4

  local value_n = buffer:range(pos0,4):le_uint()  -- todo: switch to big endian
  print( string.format("n = %d", value_n ))

  for k = 1, value_n do
    local subtree_point = subtree_p:add(manual_protocol, buffer(), "Point")
    subtree_point:add_le(field_x, buffer(pos,4))
    pos = pos+4
    subtree_point:add_le(field_y, buffer(pos,4))
    pos = pos+4
  end
end

local udp_port = DissectorTable.get("udp.port")
udp_port:add(50000, manual_protocol)
