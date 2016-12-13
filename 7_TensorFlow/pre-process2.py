from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys
import numpy as np
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def draw_char_bitmap(ch,font,char_size,x_offset,y_offset):
    image = Image.new("RGB", (char_size, char_size), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.text((x_offset, y_offset), ch, (0, 0, 0), font=font)
    gray = image.convert('L')
    bitmap = np.asarray(gray)
    return bitmap



# [chars] -> NumPy Array by font
def generate_font_bitmaps(chars, font_path, char_size, canvas_size, x_offset, y_offset):
    font_obj = ImageFont.truetype(font_path, char_size)
    bitmaps = list()
    for c in chars:
        bm = draw_char_bitmap(c, font_obj, canvas_size, x_offset, y_offset)
        bitmaps.append(bm)
    return np.array(bitmaps)


# NumPy Array -> img
def render_fonts_image(x, path, img_per_row):
    num_imgs, w, h = x.shape
    side = int(w)
    width = img_per_row * side
    height = int(np.ceil(float(num_imgs) / img_per_row)) * side
    canvas = np.zeros(shape=(height, width), dtype=np.int16)
    for idx, bm in enumerate(bitmaps):
        x = side * int(idx / img_per_row)
        y = side * int(idx % img_per_row)
        canvas[x: x + side, y: y + side] = bm
    misc.toimage(canvas).save(path)
    return path


#Processes a font into a NumPy Format
def process_font(chars,font_path,save_path,x_offset = 0,y_offset = 0,mode='target'):
    char_size = 64
    canvas = 80
    if mode == "source":
        char_size = char_size * 2
        canvas = canvas * 2
    font_bitmaps = generate_font_bitmaps(chars,font_path,char_size,canvas,x_offset,y_offset)
    _, ext = os.path.splitext(font_path)
    if not ext.lower() in [".otf", ".ttf"]:
        raise RuntimeError("unknown font type found %s. only TrueType or OpenType is supported" % ext)
    _, tail = os.path.split(font_path)
    font_name = ".".join(tail.split(".")[:-1])
    bitmap_path = os.path.join(save_path, "%s.npy" % font_name)
    np.save(bitmap_path, font_bitmaps)


#Textfile containing characters -> an array of characters
def get_chars(path):
    chars = list()
    with open(path) as f:
        for line in f:
            line = "%s" %line
            char = line.split()[0]
            chars.append(char)
    return chars


#bitmaps = generate_font_bitmaps(chars, font_path, 64, 80, 0, 0)
#render_fonts_image(bitmaps, './t4.png', 9)

# read from txt file, get a list of characters in UTF8 form
chars = get_chars('./charsets/top_3000_simplified.txt')
save_dir = "npy_for_matlab"


if __name__ ==  "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_font',type = str, default = None,
                        help = 'numpy bitmap for source font')
    parser.add_argument('--target_font',type = str,default = None,
                        help = 'numpy bitmap for target font')
    FLAGS = parser.parse_args()
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if FLAGS.source_font:
        process_font(chars,FLAGS.source_font,save_dir,0,0,mode = 'source')
    elif FLAGS.target_font:
        process_font(chars,FLAGS.target_font,save_dir,0,0,mode = 'target')


