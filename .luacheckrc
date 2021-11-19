unused_args = false
allow_defined_top = true
max_line_length = 125

globals = {
}

read_globals = {
	"DIR_DELIM", "INIT",

	"minetest", "core",
	"dump", "dump2",

	"Raycast",
	"Settings",
	"PseudoRandom",
	"PerlinNoise",
	"VoxelManip",
	"SecureRandom",
	"VoxelArea",
	"PerlinNoiseMap",
	"PcgRandom",
	"ItemStack",
	"AreaStore",

	vector = {
		fields = {
			"new",
			"equals",
			"length",
			"normalize",
			"floor",
			"round",
			"apply",
			"distance",
			"direction",
			"angle",
			"dot",
			"cross",
			"add",
			"subtract",
			"multiply",
			"divide",
			"offset",
			"sort",
			"rotate_around_axis",
			"rotate",
			"dir_to_rotation",
		},
	},

	table = {
		fields = {
			"copy",
			"indexof",
			"insert_all",
			"key_value_swap",
			"shuffle",
		},
	},

	string = {
		fields = {
			"split",
			"trim",
		},
	},

	math = {
		fields = {
			"hypot",
			"sign",
			"factorial"
		},
	},
}
