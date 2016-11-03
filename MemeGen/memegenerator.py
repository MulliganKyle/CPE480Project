# -*- coding: utf-8 -*-

import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

import sys
import os


def make_meme(topString, bottomString, filename, path='MemeGen/images'):
	# Fetches image.
	full_filename = os.path.join(path, filename)
	img = Image.open(full_filename)
	imageSize = img.size

	# Finds the biggest font size that works.
	fontSize = int(imageSize[1]/5)
	font = ImageFont.truetype("/Library/Fonts/Impact.ttf", fontSize)
	topTextSize = font.getsize(topString)
	bottomTextSize = font.getsize(bottomString)

	while (topTextSize[0] > imageSize[0]-20 or
			 bottomTextSize[0] > imageSize[0]-20):
		fontSize = fontSize - 1
		font = ImageFont.truetype("/Library/Fonts/Impact.ttf", fontSize)
		topTextSize = font.getsize(topString)
		bottomTextSize = font.getsize(bottomString)

	# Find top centered position for top text.
	topTextPositionX = (imageSize[0]/2) - (topTextSize[0]/2)
	topTextPositionY = 0
	topTextPosition = (topTextPositionX, topTextPositionY)

	# Find bottom centered position for bottom text.
	bottomTextPositionX = (imageSize[0]/2) - (bottomTextSize[0]/2)
	bottomTextPositionY = imageSize[1] - bottomTextSize[1]
	bottomTextPosition = (bottomTextPositionX, bottomTextPositionY)

	draw = ImageDraw.Draw(img)

	# TODO(kyle): Look into better method.
	# Draw outline.
	outlineRange = int(fontSize/15)
	for x in range(-outlineRange, outlineRange+1):
		for y in range(-outlineRange, outlineRange+1):
			draw.text((topTextPosition[0]+x, topTextPosition[1]+y), topString, (0,0,0), font=font)
			draw.text((bottomTextPosition[0]+x, bottomTextPosition[1]+y), bottomString, (0,0,0), font=font)
	draw.text(topTextPosition, topString, (255,255,255), font=font)
	draw.text(bottomTextPosition, bottomString, (255,255,255), font=font)

	return img


# Gets upper text in a meme image.
def get_upper(somedata):
	# Handle Python 2/3 differences in argv encoding
	result = ''
	try:
		result = somedata.decode("utf-8").upper()
	except:
		result = somedata.upper()
	return result


# Gets lower text in a meme image.
def get_lower(somedata):
	# Handle Python 2/3 differences in argv encoding
	result = ''
	try:
		result = somedata.decode("utf-8").lower()
	except:
		result = somedata.lower()		

	return result


if __name__ == '__main__':
	num_args = len(sys.argv)
	topString = ''
	meme = 'standard'

	# Check for correct number of arguments.
	if num_args < 2 or num_args > 4:
		# Incorrect number of arguments.
		print('Usage: python memegenerator.py <upper-text>')
		print('       python memegenerator.py <upper-text> <meme>')
		print('       python memegenerator.py <upper-text> <lower-text> <meme>')
		exit()

	# Parses command line arguments.
	if num_args == 2:
		# Gives upper text. Uses standard meme.
		bottomString = get_upper(sys.argv[-1])
	elif num_args == 3:
		# Gives upper text. Provides meme.
		bottomString = get_upper(sys.argv[-1])
		meme = get_lower(sys.argv[1])
	elif num_args == 4:
		# Contains  Args give meme and two lines.
		topString = get_upper(sys.argv[-2])
		bottomString = get_upper(sys.argv[-1])
		meme = get_lower(sys.argv[1])		

	# Generates meme.
	print(meme)
	filename = str(meme) + '.jpg'
	img = make_meme(topString, bottomString, filename)
	img.save("Meme.png")

