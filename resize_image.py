import PIL
from PIL import Image
import argparse

parser = argparse.ArgumentParser(description='Code for resize image')
parser.add_argument('--image_path', help='provide image path', type=str)
args = parser.parse_args()

base_width = 800
img = Image.open(args.image_path)
wpercent = (base_width / float(img.size[0]))
hsize = int((float(img.size[1]) * float(wpercent)))
img = img.resize((base_width, hsize), PIL.Image.ANTIALIAS)
img.save('resized_image.jpg')
