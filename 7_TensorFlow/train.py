import tensorflow as tf
import numpy as np
import TensorflowModel
from util import *
import os
import shutil

print ("##########################################")

########################## PARAM ##################################
# number of characters to be trained
nChars = 240
# number of characters for each iteration of training
batch_size = 16
# numer of iterations
nIter = 500
learningRate = 0.01
keepProb = 0.9

# Training Data
src_font_path = "./_TrainingData/song.npy"
tgt_font_path = "./_TrainingData/li.npy"

char_width_px = 160;
##################################################################

'''
# [nCharacter x 160 x 160]
src_chacters = np.load(src_font_path)
tgt_chacters = np.load(tgt_font_path)
'''


#Initialize FontProvider/FontManager Objects
source_font = src_font_path
target_font = tgt_font_path
split = nChars
dataset = FontDataManager(source_font, target_font, nChars, split)

# create a session for model

model = TensorflowModel.TensorflowModel(char_width_px)
model.add_block([64, 64, 1, 8])
model.add_block([16, 16, 8, 32])
model.add_block([3, 3, 32, 1])
pooled = model.pool()
dropped = model.drop_out(pooled)
convert_bitmap = tf.reshape(dropped, shape=[-1, char_width_px/2, char_width_px/2])
# to show picture
img_folder = 'frame'
if os.path.exists(img_folder):
    shutil.rmtree(img_folder)
os.mkdir(img_folder)


model.init_train_step(dropped)

model.session.run(tf.initialize_all_variables())


# run training for a batch
def train_batch(src_chars, tgt_chars):
    '''
    if (iter % int(nChars/batch_size)) == 0:
        FontProvider.getNewPerm(nChars)
    permutation, src_chars = util.extract_batch_in_order(FontProvider.current_src, batch_size, iter)
    tgt_chars = FontProvider.current_tgt[permutation, :, :]
    '''

    dic = {
        model.X: src_chars,
        model.y: tgt_chars,
        model.phase_train: True,
        model.learning_rate: 0.01,
        model.keepProb: 0.9
    }
    model.train_step.run(feed_dict = dic)
    print("Loss : {}".format(model.session.run(model.loss, feed_dict={model.X: src_chars, model.y: tgt_chars,model.phase_train: False,model.keepProb: 1.0})))


for iter in range(nIter):
    print ("\n------------------{}-------------------------".format(iter))
    src_chars, tgt_chars = dataset.next_train_batch(batch_size)
    train_batch(src_chars, tgt_chars)
    if iter % 10 == 0:
        bitmap = model.session.run(convert_bitmap, feed_dict = {model.X: src_chars,
                                                    model.y: tgt_chars,
                                                    model.phase_train: False,
                                                    model.keepProb: 1.0
                                                    })
        print ("img save as : {}".format(render_fonts_image(bitmap, img_folder, 10, iter)))
