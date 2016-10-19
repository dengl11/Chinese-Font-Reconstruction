from PIL import Image
import re
import os

# create folder if not existed
def createFolder(path):
    if not os.path.exists(path):
            os.makedirs(path)

# crop image to [mY x nX]
def crop(sourceImgPath, nX, nY, targetFolder, marginXL=0, marginXR=0, marginYT=0, marginYB=0):
    im = Image.open(sourceImgPath)
    createFolder(targetFolder)
    # name of source iamge
    sourceImgName = sourceImgPath.split('.')[-2].split('/')[-1]
    imgwidth, imgheight = im.size
    # box is (left, upper, right, lower) 
    im = im.crop((marginXL, marginYT, imgwidth-marginXR, imgheight-marginYB))

    imgwidth, imgheight = im.size
    unitX, unitY = imgwidth/nX, imgheight/nY
    for i in range(0, nX):
        for j in range(0, nY):
            box = (i*unitX, j*unitY, (i+1)*unitX, (j+1)*unitY)
            a = im.crop(box)
            try:
                a.save(os.path.join(targetFolder,"%s-%d-%d.png" %(sourceImgName, i, j)))
            except Exception as e:
                print e
                pass

# crop all images in folder to [_segmented]
def cropAllInFolder(path2folder, nx, ny, mXL=0, mXR=0, mYT=0, mYB=0):
    try:
        files = [f for f in os.listdir(path2folder) if re.match(r'[0-9]+.*\.jpg', f)]
        for img in files:
            crop(path2folder + img, nx, ny, path2folder+'_segmented/', mXL, mXR, mYT, mYB)
            print "Crop done: %s"%img
    except Exception as e:
        print "Error in cropAll: %s"%e
        pass


cropAllInFolder('../_data/3_Cursive/', 2, 3, mXL=45, mXR=45, mYT=40,mYB=40)
