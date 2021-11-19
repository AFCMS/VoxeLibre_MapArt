import math, json, os, sys

from typing import *
from PIL import Image

blocks = {}

with open("block_colors.json", "r") as block_files:
	blocks = json.loads(block_files.read())
	#print(blocks)


def vector_distance(a: Tuple[int, int, int], b: Tuple[int, int, int]) -> float:
	return math.hypot(a[0] - b[0], math.hypot(a[1] - b[1], a[2] - b[2]))


def rgb_to_nearest(color: Tuple[int, int, int]) -> str:
	assert len(color) == 3
	calculated = {}
	for b in blocks:
		calculated[b] = vector_distance(blocks[b], color)

	e: Optional[str] = None
	for b2 in calculated:
		if not e:
			e = b2
		elif calculated[b2] < calculated[e]:
			e = b2
	if e:
		return e
	else:
		return "" # air


def image_to_blocks(path: str):
	img = Image.open(path).convert("RGB")

	# flip image
	#img.transpose(Image.FLIP_LEFT_RIGHT)

	pixels = img.load()

	out: List[List[str]] = []

	for x in range(0, img.size[0]):
		ylist = []
		for y in range(0, img.size[1]):
			r, g, b = pixels[x, y]
			ylist.append(rgb_to_nearest((r, g, b)))
			ylist = ylist[::-1]
		out.append(ylist)
	
	out = out[::-1]
	print(out)
	return out

def blocks_to_we(blocks: List[List[str]]) -> str:
	out_str = ""
	for x in range(len(blocks)):
		for y in range(len(blocks[x])):
			out_str += f"\n{x} 0 {y} {blocks[x][y]} 15 0"
	return out_str


if __name__ == "__main__":
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