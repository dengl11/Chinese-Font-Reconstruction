from util import get_chars_set, ImageFont, draw_char_bitmap, np, misc
# read from txt file, get a list of characters in UTF8 form
chars = get_chars_set('./charsets/CS229.txt')
font_path = "_TrainingData/li.ttf"
save_dir = "."


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
    bitmap_path = os.path.join(save_dir, "%s.npy" % font_name)
    np.save(bitmap_path, font_bitmaps)


bitmaps = generate_font_bitmaps(chars, font_path, 64, 80, 0, 0)
render_fonts_image(bitmaps, './t4.png', 9)
