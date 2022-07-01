#!/usr/bin/env python3

import os
import re
import fire
import pathlib
import math
import json
from typing import *
from termcolor import cprint
from PIL import Image

__author__ = "AFCM"
__version__ = 1.2

"""
MineClone2 Mapart
"""

#########
# UTILS #
#########


blocks_file_path = pathlib.Path("block_colors.json")

RGB = Tuple[int, int, int]

Blocks = Dict[str, Tuple[int, int, int]]

ImageBlocks = List[List[str]]


def rgb_distance(a: RGB, b: RGB) -> float:
	return math.hypot(a[0] - b[0], math.hypot(a[1] - b[1], a[2] - b[2]))


def get_block_colors() -> Blocks:
	with open(blocks_file_path, "r") as blocks_file:
		return json.loads(blocks_file.read())


def rgb_to_nearest(blocks: Blocks, color: RGB) -> str:
	assert len(color) == 3
	calculated = {}
	for b in blocks:
		calculated[b] = rgb_distance(blocks[b], color)

	e = None
	for b2 in calculated:
		if not e:
			e = b2
		elif calculated[b2] < calculated[e]:
			e = b2
	if e:
		return e
	else:
		return ""  # air node


def image_to_blocks(path: pathlib.Path, blocks: Blocks, alpha: str = "air") -> ImageBlocks:
	img = Image.open(path).convert("RGBA")

	img = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
	img = img.rotate(180)

	pixels = img.load()

	out = []

	assert img.size[0] == 128, "Invalid image size, should be 128x"
	assert img.size[1] == 128, "Invalid image size, should be 128x"

	for x in range(0, img.size[0]):
		ylist = []
		for y in range(0, img.size[1]):
			r, g, b, a = pixels[x, y]
			if a > 0:
				ylist.append(rgb_to_nearest(blocks, (r, g, b)))
			else:
				ylist.append(alpha)
		out.append(ylist)
	return out


def blocks_to_we(blocks: ImageBlocks) -> str:
	"""
	Returns a matrix of nodes as a WorldEdit schematic string.
	"""
	out_str = ""
	for x in range(len(blocks)):
		for y in range(len(blocks[x])):
			out_str += f"\n{x} 0 {y} {blocks[x][y]} 15 0"
	return out_str


def texture_to_color(path: str) -> Optional[RGB]:
	try:
		img = Image.open(path).convert("RGBA")
		pixels = img.load()

		"""
		if "palette" in name:
			palette = []

			for y in range(0, img.size[1]):
				for x in range(0, img.size[0]):
					r, g, b, a = pixels[x, y]
					palette.append((r, g, b))

			palettes[name] = palette
		else:
		"""
		r_total = 0
		g_total = 0
		b_total = 0

		count = 0

		for x in range(0, img.size[0]):
			for y in range(0, img.size[1]):
				r, g, b, a = pixels[x, y]
				if a > 0:
					r_total += r / 255 * a
					g_total += g / 255 * a
					b_total += b / 255 * a
					count += a / 255

		average_color = None

		if count > 0:
			average_color = (
				int(r_total / count),
				int(g_total / count),
				int(b_total / count)
			)
		else:
			average_color = (255, 255, 255)

		img.close()

		return average_color

	except IOError:
		return None

# FIXME
BLOCKS_WOOL_CARPETS = re.compile(r"^mcl_wool:.*_carpet$")
BLOCKS_WOOL = re.compile(r"^mcl_wool:[a-z]*$")


def limite_blocks(pattern: Optional[re.Pattern]) -> Blocks:
	blocks = get_block_colors()
	if pattern:
		filtered_blocks = {}
		for n in blocks.keys():
			r = re.match(pattern, n)
			if r:
				filtered_blocks[n] = blocks[n]
		return filtered_blocks
	else:
		return blocks


########
# MAIN #
########


def create_map(mineclone: str, image: str, out: str, blocks: Optional[str] = None, alpha: str = "air"):
	"""
	Create a WorldEdit schematic from the given image file.
	"""

	image_path = pathlib.Path(image)
	if not image_path.exists() and image_path.is_dir():
		cprint("Image path doesn't exist!", "red")
		exit(1)

	blocks_pattern = None
	if blocks and type(blocks) == str:
		if blocks == "carpets":
			blocks_pattern = BLOCKS_WOOL_CARPETS
		elif blocks == "wool":
			blocks_pattern = BLOCKS_WOOL

	limited_blocks = limite_blocks(blocks_pattern)

	# print(json.dumps(limited_blocks))

	cprint(f"There are {len(limited_blocks)} blocks availlable", "green")

	if alpha != "air" and alpha not in limited_blocks:
		cprint("Alpha node isn't in the limited block list", "red")
		exit(1)

	out_path = pathlib.Path(out)

	cprint("Converting...", "green")

	with open(out_path, "w") as out_file:
		out_file.write(blocks_to_we(image_to_blocks(image_path, limited_blocks, alpha=alpha)))


def generate_colors(textures: str):
	"""
	Regenerate node => color mapping from given texture path.
	"""
	texture_path = pathlib.Path(textures)
	if not texture_path.exists() and not texture_path.is_dir():
		cprint("Texture path doesn't exist or isn't a folder!", "red")
		exit(1)

	colors = {}
	blocks = None

	with open("./generate_json_blocks/availlable_blocks.json") as base_blocks:
		blocks = json.loads(base_blocks.read())

	cprint("Finding files...", "green")

	file_count = 0

	for root, directories, files in os.walk(texture_path.joinpath("mods")):
		if root.endswith("/textures"):
			for name in files:
				for itemname in blocks:
					if blocks[itemname] == name:
						colors[itemname] = texture_to_color(os.path.join(root, name))
						file_count += 1

	with open("block_colors.json", "w") as colorfile:
		colorfile.write(json.dumps(colors, indent="\t"))
		colorfile.close()

	cprint(f"Files: {file_count}", "green")


fire.Fire({
	"create": create_map,
	"generate_colors": generate_colors
})
