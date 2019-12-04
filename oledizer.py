from PIL import Image
import argparse

parser = argparse.ArgumentParser(description='Turn an pixel art image into a python array for oled display')
parser.add_argument('image', metavar='Image', type=str, nargs='?',
                   help='image for processing')
parser.add_argument('--output', '-o', metavar='-o', type=str, nargs='?',
                   help='name of the output file')
parser.add_argument('--crop', '-c', action='store_true', default=False,
                    help='if the image should be cropped')
# parser.add_argument('--format', '-f', default="bytes", nargs='?', choices=['bytes', 'bool'],
#                     help='The format of the output.')

args = parser.parse_args()
print(args)

def image_to_boolean_tuple(image: Image):
    """ Gets the Image object and converts it to a matrix of booleans
    :param image: The image to be converted

    :rtype: tuple
    """
    pixels = image.load()

    width, height = image.size

    output = [width, height]

    for y in range(height):
        row = []
        for x in range(width):
            _, _, _, alpha = pixels[x, y]
            row.append(alpha > 0)
        output.append(tuple(row))
    
    return tuple(output)

def image_to_bytes(image: Image) -> bytes:
    """ Gets the Image object and converts it to tuple with widht, height and bytes with the image data
    :param image: The image to be converted

    :rtype: tuple
    """
    pixels = image.load()

    width, height = image.size

    imagebytes = bytearray()
    imagebytes.extend((width).to_bytes(2, byteorder='big'))
    imagebytes.extend((height).to_bytes(2, byteorder='big'))

    bytecounter = 0
    mbyte = 0
    for y in range(height):
        for x in range(width):
            _, _, _, alpha = pixels[x, y]
            if (alpha > 0):
                mbyte = mbyte | (1 << bytecounter)
            bytecounter = bytecounter + 1
            if bytecounter >= 8:
                imagebytes.append(mbyte)
                bytecounter = 0
                mbyte=0
    return bytes(imagebytes)

def generate_icon_file(image_file: str, output_file: str = None, crop: bool = False, output_format: str = 'bytes'):
    """ Gets an image file and converts it to a python file to be used to draw the image on
        :param image_file: the filename of the image
    
        :param output_file: filename of the output file
    
        :param crop: if the image should be cropped
    
        :param output_format: the format of the output file, bytes or bool
    """
    try:
        image = Image.open(args.image, mode='r')
    except IOError:
        print("Error loading image...")
        return

    if crop:
        image = image.crop(image.getbbox())

    output = image_to_bytes(image) if output_format == 'bytes' else image_to_boolean_tuple(image)

    if output_file is None:
        print(output)
    else:
        if not '.mpi' in output_file:
            output_file = output_file + '.mpi'
        with open(output_file, 'wb') as file:
            file.write(output)

generate_icon_file(args.image, args.output, args.crop)