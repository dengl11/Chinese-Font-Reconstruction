import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Convolution2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
K.set_image_dim_ordering('th')




#load data
li_all_data = np.load('li.npy')
song_all_data = np.load('song.npy')
#zhuan_all_data = np.load('zhuan.npy')
zhuan_all_data = np.load('zhuan.npy')
kai_all_data = np.load('kai.npy')
xing_all_data = np.load('SoftXing.npy')

# choose 100 for training from each style, 20 for testing
num_train = 500
num_test = 100

X_train = li_all_data[0:num_train,:,:]
X_train = np.concatenate((X_train,song_all_data[0:num_train,:,:]),axis=0)
X_train = np.concatenate((X_train,zhuan_all_data[0:num_train,:,:]),axis=0)
X_train = np.concatenate((X_train,kai_all_data[0:num_train,:,:]),axis=0)
X_train = np.concatenate((X_train,xing_all_data[0:num_train,:,:]),axis=0)

y_train = np.zeros((num_train,1), dtype=int)
y_train = np.concatenate((y_train, np.ones((num_train,1), dtype=int)),axis=0)
y_train = np.concatenate((y_train, 2*np.ones((num_train,1), dtype=int)),axis=0)
y_train = np.concatenate((y_train, 3*np.ones((num_train,1), dtype=int)),axis=0)
y_train = np.concatenate((y_train, 4*np.ones((num_train,1), dtype=int)),axis=0)

X_test = li_all_data[num_train:(num_train + num_test),:,:]
X_test = np.concatenate((X_test,song_all_data[num_train:(num_train + num_test),:,:]),axis=0)
X_test = np.concatenate((X_test,zhuan_all_data[num_train:(num_train + num_test),:,:]),axis=0)
X_test = np.concatenate((X_test,kai_all_data[num_train:(num_train + num_test),:,:]),axis=0)
X_test = np.concatenate((X_test,xing_all_data[num_train:(num_train + num_test),:,:]),axis=0)



y_test = np.zeros((num_test,1), dtype=int)
y_test = np.concatenate((y_test, np.ones((num_test,1), dtype=int)),axis=0)
y_test = np.concatenate((y_test, 2*np.ones((num_test,1), dtype=int)),axis=0)
y_test = np.concatenate((y_test, 3*np.ones((num_test,1), dtype=int)),axis=0)
y_test = np.concatenate((y_test, 4*np.ones((num_test,1), dtype=int)),axis=0)

#Start of real code


# fix random seed for reproducibility
seed = 7
np.random.seed(seed)


X_train = X_train.reshape(X_train.shape[0], 1, 80, 80).astype('float32')
X_test = X_test.reshape(X_test.shape[0], 1, 80, 80).astype('float32')

#normalize inputs to 0-1
X_train = X_train/255
X_test = X_test/255
# one hot encode outputs
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
num_classes = y_test.shape[1]



def baseline_model():
    #create model
    model = Sequential()
    model.add(Convolution2D(32, 5, 5, border_mode='valid', input_shape=(1, 80, 80), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))
    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

model = baseline_model()
# Fit the model
model.fit(X_train, y_train, validation_data=(X_test, y_test), nb_epoch=10, batch_size=100, verbose=2)
# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Baseline Error: %.2f%%" % (100-scores[1]*100))
#model.predict(X_test)



