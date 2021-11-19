import json, os, sys

from typing import *
from PIL import Image
#from pathlib import Path

colors = {}
palettes = {}

mcl2_path = None

try:
	mcl2_path = sys.argv[1]
except IndexError:
	print("Provide the MineClone2 path to the script as an argument")
	exit(1)

blocks = None

with open("./generate_json_blocks/availlable_blocks.json") as base_blocks:
	blocks = json.loads(base_blocks.read())
	#print(blocks)

def texture_to_color(path: str) -> Tuple[int]:
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
			average_color = (int(r_total / count), int(g_total / count), int(b_total / count))
		else:
			average_color = (255, 255, 255)

		return average_color

		img.close()
	except IOError:
		pass

print("Finding files...")

file_count = 0
for root, directories, files in os.walk(mcl2_path+"/mods"):
	if root.endswith("/textures"):
		for name in files:
			for itemname in blocks:
				if blocks[itemname] == name:
					colors[itemname] = texture_to_color(os.path.join(root, name))
					file_count += 1


with open("block_colors.json", "w") as colorfile:
	colorfile.write(json.dumps(colors))
	colorfile.close()

print(f"Files: {file_count}")

#with open("palettes.json", "w") as palettefile:
#	palettefile.write(json.dumps(palettes))

