-- https://mika-s.github.io/wireshark/lua/dissector/2017/11/04/creating-a-wireshark-dissector-in-lua-1.html
-- https://mika-s.github.io/topics/
-- sudo wireshark -X lua_script:manual.lua 
-- reload: ctrl-shift-L
-- cool: https://mika-s.github.io/wireshark/lua/dissector/usb/2019/07/23/creating-a-wireshark-usb-dissector-in-lua-1.html
-- https://sharkfestus.wireshark.org/sharkfest.09/DT06_Bjorlykke_Lua%20Scripting%20in%20Wireshark.pdf
-- https://users.informatik.haw-hamburg.de/~schulz/pub/Rechnernetze/tools/wireshark/WiresharkFullDocumentation.pdf

manual_protocol = Proto("MyManualProto",  "My Manual Protocol")

local point = require("point.point")
local polygon = require("polygon.polygon")

manual_protocol.fields = {}
for _,f in ipairs(polygon.polygon_fields) do table.insert(manual_protocol.fields, f) end
for _,f in ipairs(point.point_fields) do table.insert(manual_protocol.fields, f) end

function manual_protocol.dissector(buffer, pinfo, tree)
  pinfo.cols.protocol = manual_protocol.name
  polygon.dissector_polygon(manual_protocol, buffer, 0, tree)
end

local udp_port = DissectorTable.get("udp.port")
udp_port:add(50000, manual_protocol)
