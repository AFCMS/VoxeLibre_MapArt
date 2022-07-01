local minetest = minetest

local pairs = pairs

local modpath = minetest.get_modpath(minetest.get_current_modname())

local color_textures = {}

minetest.register_on_mods_loaded(function()
	for name, def in pairs(minetest.registered_nodes) do
		if name == "mcl_core:bedrock" then break end
		if (minetest.get_item_group(name, "building_block") ~= 0 or
			minetest.get_item_group(name, "carpet") ~= 0)
			and minetest.get_item_group(name, "not_in_creative_inventory") == 0 then
			if def.tiles and type(def.tiles) == "table" then
				if type(def.tiles[1]) == "table" then
					color_textures[name] = def.tiles[1].name
				else
					color_textures[name] = def.tiles[1]
				end
			elseif def.tiles and type(def.tiles) == "string" then
				color_textures[name] = def.tiles
			end
		end
	end
	local file = assert(io.open(modpath .. "/availlable_blocks.json", "w"))
	file:write(minetest.write_json(color_textures, true))
	file:close()
	minetest.request_shutdown("Blocks Generated!")
end)