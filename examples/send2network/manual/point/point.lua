field_x = ProtoField.float("x", "x", base.DEC)
field_y = ProtoField.float("y", "y", base.DEC)

m={}

m.point_fields = { field_x, field_y }

function m.dissector_point(proto, buffer, pos, tree)
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
  
  return m;