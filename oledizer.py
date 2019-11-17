from PIL import Image
import argparse

parser = argparse.ArgumentParser(description='Turn an pixel art image into a python array for oled display')
parser.add_argument('image', metavar='Image', type=str, nargs='?',
                   help='image for processing')
parser.add_argument('--output', '-o', metavar='-o', type=str, nargs='?',
                   help='name of the output file')
parser.add_argument('--crop', '-c', action='store_true', default=False,
                    help='if the image should be cropped')


args = parser.parse_args()
print(args)

def image_to_boolean_array(image):
    pixels = image.load()

    width, height = image.size

    output = []

    for y in range(height):
        row = []
        for x in range(width):
            _, _, _, alpha = pixels[x, y]
            row.append(alpha > 0)
        output.append(tuple(row))
    
    return output

def generate_icon_file(image_file, output_file=None, crop=False):
    try:
        image = Image.open(args.image, mode='r')
    except IOError:
        print("Error loading image...")
        return

    if crop:
        image = image.crop(image.getbbox())

    output = image_to_boolean_array(image)

    if output_file is None:
        print(output)
    else:
        with open(output_file + '.py', 'w') as file:
            file.write(output_file + ' = ')
            file.write(str(tuple(output)))

generate_icon_file(args.image, args.output, args.crop)