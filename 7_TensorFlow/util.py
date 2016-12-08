import numpy as np
import scipy.misc as misc
import os

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
