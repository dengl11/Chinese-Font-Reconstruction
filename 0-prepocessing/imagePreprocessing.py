from skimage import io
import numpy as np
import skimage

# this part converts a picture into a matrix whose size is the same as the picture and 
# if a certain is filled with black, the element of the same location in the matrix is 
# stored as "true", otherwisem it is "false"
im = skimage.io.imread('zheng.jpg')
imshape = im.shape
newshape = (imshape[0], imshape[1])

newim_gray = np.empty(shape = newshape, dtype = 'int')
newim_bool = np.empty(shape = newshape, dtype = 'bool')
newim_binary = im # pass by reference

for row in xrange(imshape[0]):
    for col in xrange(imshape[1]):
        newim_gray[row, col] = (int(im[row,col,0])+int(im[row,col,1])+int(im[row,col,2]))/3
        if (newim_gray[row, col]) < 255/2:
            newim_bool[row, col] =  True
            for i in xrange(3):
                newim_binary[row,col,i] = 0
        else:
            newim_bool[row, col] =  False
            for i in xrange(3):
                newim_binary[row,col,i] = 255
          
#  this part is for checking result
#    print newim_bool    
#count = 0
#for row in xrange(imshape[0]):
#    for col in xrange(imshape[1]):
#        if (newim_bool[row, col]):
#            count = count + 1
#            
#print count
#
skimage.io.imsave('zheng_vertical2.jpg',im)

