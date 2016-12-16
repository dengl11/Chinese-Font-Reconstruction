import tensorflow as tf
import numpy as np
import TensorflowModel
from util import *
import os
import shutil

print ("##########################################")

########################## PARAM ##################################
src, tgt = "song", "li"
# number of characters to be trained
nChars = 3000
# number of characters for each iteration of training
batch_size = 16
# numer of iterations
nIter = 2000
learningRate = 0.01
keepProb = 0.9

# number of layer for each group
layers = 3

# Training Data
train_src_path = "./_PreprocessResult/%s.npy"%src
train_tgt_path = "./_PreprocessResult/%s.npy"%tgt

# Validation
validation_src_path = "./_PreprocessResult/%s.npy"%src
validation_tgt_path = "./_PreprocessResult/%s.npy"%tgt
# Validation
validation_src_chars = read_font_data("./_Validation/%s.npy"%src, True)
validation_tgt_chars = read_font_data("./_Validation/%s.npy"%tgt, True)

#Summary Directory
summary_dir = "./Summary"



char_width_px = 160;
##################################################################

#Initialize FontProvider/FontManager Objects
split = nChars
dataset = FontDataManager(train_src_path, train_tgt_path, nChars, split)

# create a session for model

model = TensorflowModel.TensorflowModel(char_width_px)

model.add_block([64,64,1,8])
model.add_block_group([64, 64, 8, 8], layers-1)
model.add_block([16,16,8,32])
model.add_block_group([16, 16, 32,32], layers-1)
model.add_block([7,7,32,32])
model.add_block_group([7,7,32,32],layers-1)
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
    # RUN TRAINING
    model.train_step.run(feed_dict = dic)
    # CALCULATE TRAINING LOSS
    train_loss = model.session.run(model.loss, feed_dict={model.X: src_chars, model.y: tgt_chars,model.phase_train: False,model.keepProb: 1.0})
    # CALCULATE VALIDATION LOSS
    validation_loss = model.session.run(model.loss, feed_dict={model.X: validation_src_chars, model.y: validation_tgt_chars,model.phase_train: False,model.keepProb: 1.0})
    print("Train Loss : {} | Validation Loss: {}".format(train_loss, validation_loss))


for iter in range(nIter):
    print ("\n------------------{}-------------------------".format(iter))
    src_chars, tgt_chars = dataset.next_train_batch(batch_size)
    train_batch(src_chars, tgt_chars)
    if iter % 100 == 0:
        bitmap = model.session.run(convert_bitmap, feed_dict = {model.X: validation_src_chars,
                                                    model.y: validation_tgt_chars,
                                                    model.phase_train: False,
                                                    model.keepProb: 1.0
                                                    })
        print ("img save as : {}".format(render_fonts_image(bitmap, img_folder, 10, iter)))

gif = compile_frames_to_gif(img_folder, os.path.join(img_folder, "transition.gif"))
print "==============COMPLETED!================="
print("gif saved at %s" % gif)
print "========================================="
