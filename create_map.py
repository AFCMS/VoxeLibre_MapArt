import math, json, os, sys

from typing import *
from PIL import Image
# TODO: rotate images by 180

blocks = {}

with open("block_colors.json", "r") as block_files:
	blocks = json.loads(block_files.read())
	#print(blocks)


def vector_distance(a: Tuple[int, int, int], b: Tuple[int, int, int]) -> float:
	return math.hypot(a[0] - b[0], math.hypot(a[1] - b[1], a[2] - b[2]))


def rgb_to_nearest(color: Tuple[int, int, int]) -> Optional[str]:
	assert len(color) == 3
	calculated = {}
	for b in blocks:
		calculated[b] = vector_distance(blocks[b], color)

	e = None
	for b2 in calculated:
		if not e:
			e = b2
		elif calculated[b2] < calculated[e]:
			e = b2
	#print("out="+e)
	#print(calculated[e])
	return e


def image_to_blocks(path: str):
	img = Image.open(path).convert("RGB")
	pixels = img.load()

	out = [i for i in range(img.size[1])]

	for x in range(0, img.size[0]):
		ylist = [i for i in range(img.size[0])]
		for y in range(0, img.size[1]):
			r, g, b = pixels[x, y]
			ylist[y] = rgb_to_nearest((r, g, b))
		out[x] = ylist
	
	return out

def blocks_to_we(blocks: List[List[str]]) -> str:
	out_str = ""
	for x in range(len(blocks)):
		for y in range(len(blocks[x])):
			out_str += f"\n{x} 0 {y} {blocks[x][y]} 15 0"
	return out_str


if __name__ == "__main__":
	print('Number of arguments:', len(sys.argv), 'arguments.')

	if len(sys.argv) == 0:
		print("No arguments was passed to the script!")
		exit(1)
	elif len(sys.argv) > 3:
		print("Too many arguments was passed to the script!")
		exit(2)

	image_path = sys.argv[1]
	out_path = sys.argv[2]

	print("Converting...")

	shem = blocks_to_we(image_to_blocks(image_path))

	with open(out_path, "w") as out_file:
		out_file.write(shem)
	
	print("Schematic saved at " + out_path)