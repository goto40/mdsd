-- https://mika-s.github.io/wireshark/lua/dissector/2017/11/04/creating-a-wireshark-dissector-in-lua-1.html
-- https://mika-s.github.io/topics/
-- sudo wireshark -X lua_script:manual.lua 
-- reload: ctrl-shift-L
-- cool: https://mika-s.github.io/wireshark/lua/dissector/usb/2019/07/23/creating-a-wireshark-usb-dissector-in-lua-1.html
-- https://sharkfestus.wireshark.org/sharkfest.09/DT06_Bjorlykke_Lua%20Scripting%20in%20Wireshark.pdf
-- https://users.informatik.haw-hamburg.de/~schulz/pub/Rechnernetze/tools/wireshark/WiresharkFullDocumentation.pdf

manual_protocol = Proto("MyManualProto",  "My Manual Protocol")

field_x = ProtoField.float("x", "x", base.DEC)
field_y = ProtoField.float("y", "y", base.DEC)
point_fields = { field_x, field_y }

field_n = ProtoField.uint32("n", "n", base.DEC)
field_c = ProtoField.uint8("c", "c", base.DEC)
polygon_fields = { field_c, field_n }

manual_protocol.fields = {}
for _,f in ipairs(polygon_fields) do table.insert(manual_protocol.fields, f) end
for _,f in ipairs(point_fields) do table.insert(manual_protocol.fields, f) end

function dissector_point(proto, buffer, pos, tree)
  length = buffer:len()
  if length == 0 then return end
  if length == pos then return end

  local subtree_point = tree:add(proto, buffer(), "Point")

  subtree_point:add_le(field_x, buffer(pos,4))
  pos = pos+4
  subtree_point:add_le(field_y, buffer(pos,4))
  pos = pos+4
  return pos
end

function dissector_polygon(proto, buffer, pos, tree)
  length = buffer:len()
  if length == 0 then return end
  if length == pos then return end

  local subtree = tree:add(proto, buffer(), "Polygon")

  pos0 = pos;

  subtree:add_le(field_n, buffer(pos,4))
  pos = pos + 4

  local subtree_p = subtree:add(proto, buffer(), "Points p")

  local value_n = buffer:range(pos0,4):le_uint()  -- todo: switch to big endian
  -- print( string.format("n = %d", value_n ))

  for k = 1, value_n do
    pos = dissector_point(proto, buffer, pos, subtree_p)
  end

  local subtree_c = subtree:add(proto, buffer(), "xxx")
  for k = 1, 100 do
    subtree_c:add_le(field_c, buffer(pos,1))
    pos = pos+1
  end

  return pos
end

function manual_protocol.dissector(buffer, pinfo, tree)
  pinfo.cols.protocol = manual_protocol.name
  dissector_polygon(manual_protocol, buffer, 0, tree)
end

local udp_port = DissectorTable.get("udp.port")
udp_port:add(50000, manual_protocol)
