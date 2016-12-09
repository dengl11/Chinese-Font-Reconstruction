# -*- coding: utf-8 -*-
import numpy as np
import scipy.misc as misc
import os

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




'''
# normalize value of pixel to [0, 1]
def normalize_pix(img, limit = 255.0):
    return img/limit;

# randomly extract batch_size of characters from characters
# return (permutation, batich_characters)
def extract_batch(characters, batch_size):
    chars_index = range(len(characters))
    # randomely permuate
    np.random.shuffle(chars_index)
    return (chars_index[0:batch_size], characters[chars_index][0:batch_size, :, :])

def extract_batch_in_order(characters, batch_size, iter):
    nChar = len(characters)
    subset = range(batch_size*iter%nChar, batch_size*(iter+1)%nChar)
    return  (subset, characters[subset])





class FontProvider(object):
    def __init__(self,source,target,nChars):
        permutation, src_chacters = extract_batch(source, nChars)
        tgt_chacters = target[permutation, :, :]
        src_chacters = normalize_pix(src_chacters)
        tgt_chacters = normalize_pix(tgt_chacters)
        self.src = src_chacters
        self.target = tgt_chacters

    def getNewPerm(self,nChars):
        permutation, src_chacters = extract_batch(self.src, nChars)
        tgt_chacters = self.target[permutation, :, :]
        self.current_src = src_chacters
        self.current_tgt = tgt_chacters
'''
