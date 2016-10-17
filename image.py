import skimage
import numpy as np



im = skimage.io.imread('good.jpg')
imshape = im.shape
newshape = (imshape[0], imshape[1])
count = 0
newim_gray = np.empty(shape = newshape, dtype = 'int')
newim_bool = np.empty(shape = newshape, dtype = 'bool')
for row in xrange(imshape[0]):
    for col in xrange(imshape[1]):
        newim_gray[row, col] = (int(im[row,col,0])+int(im[row,col,1])+int(im[row,col,2]))/3
        if (newim_gray[row, col]) < 255/2:
            newim_bool[row, col] =  True           
        else:
            newim_bool[row, col] =  False

#for row in xrange(imshape[0]):
#    for col in xrange(imshape[1]):
#        if (newim_bool[row, col]):
#            count = count + 1
#            
#print count