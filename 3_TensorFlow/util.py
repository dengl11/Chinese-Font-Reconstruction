# -*- coding: utf-8 -*-
import numpy as np
import glob
import scipy.misc as misc
import os
import imageio
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def compile_frames_to_gif(frame_dir, gif_file):
    frames = sorted(glob.glob(os.path.join(frame_dir, "*.png")))
    images = [imageio.imread(f) for f in frames]
    imageio.mimsave(gif_file, images, duration=0.1)
    return gif_file


def render_fonts_image(bitmap, path, img_per_row, step):
    # scale 0-1 matrix back to gray scale bitmaps
    bitmap_denormalized = (bitmap * 255.).astype(dtype=np.int16) % 256

    img_path = os.path.join(path, "step_%04d.png" % step)
    num_imgs, w, h = bitmap.shape
    assert w == h
    side = int(w)
    width = img_per_row * side
    height = int(np.ceil(float(num_imgs) / img_per_row)) * side
    canvas = np.zeros(shape=(height, width), dtype=np.int16)
    # make the canvas all white
    canvas.fill(255)
    for idx, bm in enumerate(bitmap_denormalized):
        x = side * int(idx / img_per_row)
        #bitmap = side * int(idx / img_per_row)
        y = side * int(idx % img_per_row)
        canvas[x: x + side, y: y + side] = bm
    misc.toimage(canvas).save(img_path)
    return img_path



def read_font_data(font, unit_scale):
    F = np.load(font)
    if unit_scale:
        return F / 255.
    return F


class FontDataProvider(object):
    def __init__(self, font, start, end):
        self.start = start
        self.end = end
        self.data = np.copy(font[start: end])
        self.cursor = 0
        self.length = self.end - self.start

    def get_data(self):
        return self.data

    def next_batch(self, batch_size):
        if self.cursor >= self.length:
            self.cursor = 0
        batch_start = self.cursor
        batch_end = self.cursor + batch_size
        self.cursor += batch_size
        return self.data[batch_start: batch_end]


class FontDataManager(object):
    def __init__(self, src, target, total, split_point, unit_scale=True, shuffle=False):
        src_data = read_font_data(src, unit_scale) # same as ours
        target_data = read_font_data(target, unit_scale)
        if shuffle: # change order of src and target
            perm = np.arange(src_data.shape[0])
            np.random.shuffle(perm)
            src_data = src_data[perm]
            target_data = target_data[perm]
        self.train_source = FontDataProvider(src_data, 0, split_point)
        self.validation_source = FontDataProvider(src_data, split_point, total)
        self.train_target = FontDataProvider(target_data, 0, split_point)
        self.validation_target = FontDataProvider(target_data, split_point, total)

    def next_train_batch(self, batch_size):
        if self.train_source.cursor >= self.train_source.length:
            # random shuffle the training examples
            # otherwise the model's performance fluctuate periodically
            perm = np.arange(self.train_source.length)
            np.random.shuffle(perm)
            self.train_source.data = self.train_source.data[perm]
            self.train_target.data = self.train_target.data[perm]
        return self.train_source.next_batch(batch_size), self.train_target.next_batch(batch_size)

    def get_validation(self):
        return self.validation_source.get_data(), \
               self.validation_target.get_data()






def draw_char_bitmap(ch, font, char_size, x_offset, y_offset):
    image = Image.new("RGB", (char_size, char_size), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.text((x_offset, y_offset), ch, (0, 0, 0), font=font)
    gray = image.convert('L')
    bitmap = np.asarray(gray)
    return bitmap

def generate_font_bitmaps(chars, font_path, char_size, canvas_size, x_offset, y_offset):
    font_obj = ImageFont.truetype(font_path, char_size)
    bitmaps = list()
    for c in chars:
        bm = draw_char_bitmap(c, font_obj, canvas_size, x_offset, y_offset)
        bitmaps.append(bm)
    return np.array(bitmaps)


def process_font(chars, font_path, save_dir, x_offset=0, y_offset=0, mode='target'):
    char_size = 64
    canvas = 80
    if mode == 'source':
        char_size *= 2
        canvas *= 2
    font_bitmaps = generate_font_bitmaps(chars, font_path, char_size,
                                         canvas, x_offset, y_offset)
    _, ext = os.path.splitext(font_path)
    if not ext.lower() in [".otf", ".ttf"]:
        raise RuntimeError("unknown font type found %s. only TrueType or OpenType is supported" % ext)
    _, tail = os.path.split(font_path)
    font_name = ".".join(tail.split(".")[:-1])
    bitmap_path = os.path.join(save_dir, "%s.npy" % font_name)
    np.save(bitmap_path, font_bitmaps)
    sample_image_path = os.path.join(save_dir, "%s_sample.png" % font_name)
    render_fonts_image(font_bitmaps[:9], sample_image_path, 9, False)
    print("%s font %s saved at %s" % (mode, font_name, bitmap_path))


def get_chars_set(path):
    """
    Expect a text file that each line is a char
    """
    chars = list()
    with open(path) as f:
        for line in f:
            line = u"%s" % line
            char = line.split()[0]
            chars.append(char)
    return chars


def render_chars(chars, font_path, save_dir, x_offset=0, y_offset=0):
    char_size = 64
    canvas = 80
    font_bitmaps = generate_font_bitmaps(chars, font_path, char_size,
                                         canvas, x_offset, y_offset)
    print font_bitmaps
    _, tail = os.path.split(font_path)
    font_name = ".".join(tail.split(".")[:-1])
    bitmap_path = os.path.join(save_dir, "%s.npy" % font_name)
    np.save(bitmap_path, font_bitmaps)
    sample_image_path = os.path.join(save_dir, "%s.png" % font_name)
    bitmap2img(font_bitmaps[:9], sample_image_path, 9)

def bitmap2img(bitmap, img_path, img_per_row):
    # scale 0-1 matrix back to gray scale bitmaps
    bitmap_denormalized = (bitmap * 255.).astype(dtype=np.int16) % 256
    num_imgs, w, h = bitmap.shape
    assert w == h
    side = int(w)
    width = img_per_row * side
    height = int(np.ceil(float(num_imgs) / img_per_row)) * side
    canvas = np.zeros(shape=(height, width), dtype=np.int16)
    # make the canvas all white
    canvas.fill(255)
    for idx, bm in enumerate(bitmap_denormalized):
        bitmap = side * int(idx / img_per_row)
        y = side * int(idx % img_per_row)
        canvas[bitmap: bitmap + side, y: y + side] = bm
    misc.toimage(canvas).save(img_path)
    return img_path
