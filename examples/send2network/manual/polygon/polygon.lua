field_n = ProtoField.uint32("n", "n", base.DEC)
field_c = ProtoField.uint8("c", "c", base.ENC_ASCII)

local point = require("point.point")

m={}

m.polygon_fields = { field_c, field_n }

function m.dissector_polygon(proto, buffer, pos, tree)
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
    pos = point.dissector_point(proto, buffer, pos, subtree_p)
  end

  local subtree_c = subtree:add(proto, buffer(), "string=" .. buffer(pos,4):stringz())
  for k = 1, 100 do
    subtree_c:add_le(field_c, buffer(pos,1))
    pos = pos+1
  end

  return pos
end

return m;
