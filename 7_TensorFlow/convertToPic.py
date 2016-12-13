
import numpy as np
import scipy.misc as misc
import os
#from PIL import Image
#from PIL import ImageDraw
#from PIL import ImageFont
import shutil
import argparse



def convToPics(font_type,true_size = 80):
    #Converts a (n by x by x) numpy array to n pictures
    #Saves the pictures to the corresponding folder based
    #on their font type
    #os.mkdir("%s_pics" % font_type)
    npy_array = np.load("./npy_for_matlab/%s.npy" % font_type)
    save_path = "matlab_pics/%s_pics" % font_type
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    for i in range(npy_array.shape[0]):
        render_fonts_image(npy_array[i],save_path,i,font_type,true_size)


def render_fonts_image(bitmap, path, index,font,true_size):
    img_path = os.path.join(path, "%s_%04d.png" % (font,index))
    width, height = bitmap.shape
    image = bitmap[0:true_size,0:true_size]
    misc.toimage(image).save(img_path)
    return img_path



if __name__ ==  "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--font_type',type = str, default = None,
                        help = 'font to convert (from npy to pics)')
    FLAGS = parser.parse_args()
    convToPics(FLAGS.font_type)



