from util import get_chars_set, ImageFont, draw_char_bitmap, np, misc


def render_sample(chars, font_path, save_path):
    bitmaps = generate_font_bitmaps(chars, font_path, 64, 80, 0, 0)
    render_fonts_image(bitmaps, save_path, 9)

# [chars] -> NumPy Array by font
def generate_font_bitmaps(chars, font_path, char_size, canvas_size, x_offset=0, y_offset=0):
    font_obj = ImageFont.truetype(font_path, char_size)
    bitmaps = list()
    for c in chars:
        bm = draw_char_bitmap(c, font_obj, canvas_size, x_offset, y_offset)
        bitmaps.append(bm)
    return np.array(bitmaps)


# NumPy Array -> img
def render_fonts_image(x, path, img_per_row):
    bitmaps = x
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


#src, tgt = "song", "li"
src, tgt = "song", "SoftXing"
src_font_path = "_SourceData/%s.ttf"%src
tgt_font_path = "_SourceData/%s.ttf"%tgt

# read from txt file, get a list of characters in UTF8 form
#validation_chars = get_chars_set('./_Validation/validation_chars_3_line.txt')
#validation_chars = get_chars_set('./_Validation/fullText.txt')
validation_chars = get_chars_set('./_Validation/validation_chars.txt')
train_chars = get_chars_set('./_SourceData/charsets/top_3000_simplified.txt')

# render sample images about source and target fonts
render_sample(validation_chars, src_font_path, '_Validation/%s.png'%src)
render_sample(validation_chars, tgt_font_path, '_Validation/%s.png'%tgt)

# save the npy file for source and target fonts for TRAINING
src_bitmap = generate_font_bitmaps(train_chars, src_font_path, 64*2, 80*2)
tgt_bitmap = generate_font_bitmaps(train_chars, tgt_font_path, 64, 80)
np.save("./_PreprocessResult/%s.npy"%src, src_bitmap,)
np.save("./_PreprocessResult/%s.npy"%tgt, tgt_bitmap)

# save the npy file for source and target fonts for VALIDATION
src_bitmap = generate_font_bitmaps(validation_chars, src_font_path, 64*2, 80*2)
tgt_bitmap = generate_font_bitmaps(validation_chars, tgt_font_path, 64, 80)
np.save("./_Validation/%s.npy"%src, src_bitmap,)
np.save("./_Validation/%s.npy"%tgt, tgt_bitmap)
