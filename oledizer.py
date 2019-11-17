from PIL import Image
import argparse

parser = argparse.ArgumentParser(description='Turn an pixel art image into a python array for oled display')
parser.add_argument('image', metavar='Image', type=str, nargs='+',
                   help='image for processing')
parser.add_argument('--output', metavar='-o', type=str, nargs='+',
                   help='name of the output file')

args = parser.parse_args()

print(args.image)

try:
    image = Image.open(args.image[0], mode='r')
except:
    print("Error loading image...")
    

pixels = image.load()

width, height = image.size

output = []

for y in range(height):
    row = []
    for x in range(width):
        r, g, b, a = pixels[x, y]
        row.append(a > 0)
    output.append(row.copy())

print(output)


