import tensorflow as tf
import numpy as np
import TensorflowModel
import util
import os
import shutil

print "##########################################"


########################## PARAM ##################################
# number of characters to be trained
nChars = 200
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

# [nCharacter x 160 x 160]
src_chacters = np.load(src_font_path)
tgt_chacters = np.load(tgt_font_path)

# extract real training chars | from now on, training data becomes nChars
permutation, src_chacters = util.extract_batch(src_chacters, nChars)
tgt_chacters = tgt_chacters[permutation, :, :]

# normalize
src_chacters = util.normalize_pix(src_chacters)
tgt_chacters = util.normalize_pix(tgt_chacters)

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
def train_batch(iter):
    permutation, src_chars = util.extract_batch_in_order(src_chacters, batch_size, iter)
    tgt_chars = tgt_chacters[permutation, :, :]
    dic = {
        model.X: src_chars,
        model.y: tgt_chars,
        model.phase_train: True
    }
    model.train_step.run(feed_dict = dic )
    print "Loss : {}".format(model.session.run(model.loss, feed_dict=dic))




for iter in range(nIter):
    print "\n------------------{}-------------------------".format(iter)
    train_batch(iter)
    if iter % 10 == 0:
        bitmap = model.session.run(convert_bitmap, feed_dict = {model.X: src_chacters[0:10,:,:],
                                                    model.y: tgt_chacters[0:10,:,:],
                                                    model.phase_train: False
                                                    })
        print "img save as : {}".format(util.render_fonts_image(bitmap, img_folder, 10, iter))
