#run imagePreprocessing before running this file

# for the character as a whole
def getHeightWidthRatio(im_bool):
    assert(getLowestCoordinate(im_bool)[0] != None)    
    height = getLowestCoordinate(im_bool)[0] - getUppermostCoordinate(im_bool)[0]
    width = getRightmostCoordinate(im_bool)[1] - getLeftmostCoordinate(im_bool)[1]
    assert(width != 0)
    return height / (width + 0.0)



## for dots
# Height Width Ratio of a dot, treating the dot as a whole
def getDotHeightWidthRatio(im_bool_dot):
    return getHeightWidthRatio(im_bool_dot) # reuse the function getHeightWidthRatio(im_bool)

# ratio of the dot's head height and Tail height
def getDotHeadTailRatio(im_bool_dot):
    assert(getLeftmostCoordinate(im_bool_dot)[0] != None) 
    leftMostCol = getLeftmostCoordinate(im_bool_dot)[1]
    rightMostCol = getRightmostCoordinate(im_bool_dot)[1]
    width = rightMostCol - leftMostCol
    leftCheckPoint = int(leftMostCol + width * 0.10)    
    rightCheckPoint = int(rightMostCol - width * 0.10)    
    headHeight = 0
    for r in xrange(im_bool_dot.shape[0]):    
        if im_bool_dot[r,leftCheckPoint] and not isPotentialNoisePoint(im_bool_dot, r, leftCheckPoint):
            headHeight += 1
            
    TailHeight = 0
    for r in xrange(im_bool_dot.shape[0]):    
        if im_bool_dot[r,rightCheckPoint] and not isPotentialNoisePoint(im_bool_dot, r, rightCheckPoint):
            TailHeight += 1  
    assert(TailHeight != 0)
    print headHeight, TailHeight
    return headHeight / (TailHeight + 0.0)       
              
              
              
## for horizontals
def getSlopes_horizontal(im_bool_horizontal):                
    numRows = im_bool_horizontal.shape[0]
    assert(getLeftmostCoordinate(im_bool_horizontal)[0] != None) 
    leftMostCol = getLeftmostCoordinate(im_bool_horizontal)[1]
    rightMostCol = getRightmostCoordinate(im_bool_horizontal)[1]
    width = rightMostCol - leftMostCol
    numSeg = 10
    result = range(numSeg)
    for i in xrange(numSeg):
        start = leftMostCol + i*width/(numSeg)
        end = leftMostCol + (i+1)*width/(numSeg)
        result[i] = getOneSlopeHorizontal(im_bool_horizontal, numRows, start, end)
    return result

def getOneSlopeHorizontal(im_bool_horizontal, numRows, startCol, endCol):
    startMidHeight = getMidHeightOrThicknessInHeight(im_bool_horizontal,numRows, startCol) 
    endMidHeight = getMidHeightOrThicknessInHeight(im_bool_horizontal,numRows, endCol)  
    return (endMidHeight - startMidHeight)/(endCol - startCol + 0.0)
    
        
# the midPoint of a column being fill or the difference of lower point and higher point
#  0: 0     
#  1: 1
#  2: 1
#  3: 1
#  4: 0
#  for the column above, midHeight is (1+3)/2 = 2, and thickness in height is 3-1+1= 3     
def getMidHeightOrThicknessInHeight(im_bool,numRows, col, calMidHeight = True):
    r = 0
    while r < numRows and (not im_bool[r,col] or isPotentialNoisePoint(im_bool, r, col)):
        r += 1
    higherR = r
    while r < numRows and (im_bool[r,col] and not isPotentialNoisePoint(im_bool, r, col)):
        r += 1
    lowerR = r
    if calMidHeight:
        return (higherR + lowerR)/2
    else:
        return higherR - lowerR + 1


## for Verticals
def getSlopes_vertical(im_bool_vertical):                
    numCols = im_bool_vertical.shape[1]
    assert(getLeftmostCoordinate(im_bool_vertical)[0] != None) 
    upperMostRow = getUppermostCoordinate(im_bool_vertical)[0]
    lowestRow = getLowestCoordinate(im_bool_vertical)[0]
    height = lowestRow - upperMostRow
    numSeg = 10
    result = range(numSeg)
    for i in xrange(numSeg):
        start = upperMostRow + i*height/(numSeg)
        end = upperMostRow + (i+1)*height/(numSeg)
        result[i] = getOneSlopeVertical(im_bool_vertical, numCols, start, end)
    return result

def getOneSlopeVertical(im_bool_vertical, numCols, startRow, endRow):
    startMidWidth = getMidWidth(im_bool_vertical,numCols, startRow) 
    endMidWidth = getMidWidth(im_bool_vertical,numCols, endRow)  
    return (endMidWidth - startMidWidth)/(endRow - startRow + 0.0)


# the midPoint of a column being fill            
def getMidWidth(im_bool,numCols, row):
    c = 0
    while c < numCols and (not im_bool[row,c] or isPotentialNoisePoint(im_bool, row,c)):
        c += 1
    leftC = c
    while c < numCols and (im_bool[row,c] and not isPotentialNoisePoint(im_bool, row,c)):
        c += 1
    rightC = c
    return (leftC + rightC)/2


##for throw-away and press-down
def getThicknessChanges(im_bool):
    numRows = im_bool.shape[0]
    assert(getLeftmostCoordinate(im_bool)[0] != None) 
    leftMostCol = getLeftmostCoordinate(im_bool)[1]
    rightMostCol = getRightmostCoordinate(im_bool)[1]
    leftCheckPoint = int(leftMostCol + (rightMostCol - leftMostCol) * 0.05)    
    rightCheckPoint = int(rightMostCol - (rightMostCol - leftMostCol) * 0.05)   
    width = rightCheckPoint - leftCheckPoint
    numSeg = 10
    startThickness = getMidHeightOrThicknessInHeight(im_bool,numRows, leftCheckPoint, False)
    result = range(numSeg)
    for i in xrange(numSeg):
        thickness = getMidHeightOrThicknessInHeight(im_bool,numRows, leftCheckPoint+ i*width/(numSeg - 1), False)   
        result[i] = thickness/(startThickness + 0.0)
    return result
    

    
## for all images
def getLeftmostCoordinate(im_bool):
    numRows = im_bool.shape[0]
    numCols = im_bool.shape[1]
    for c in xrange(numCols): 
        for r in xrange(numRows):    
            if im_bool[r,c] and not isPotentialNoisePoint(im_bool, r, c):
                return (r,c)
    return (None, None)  # client should assert None
    

def getRightmostCoordinate(im_bool):
    numRows = im_bool.shape[0]
    numCols = im_bool.shape[1]
    for c in xrange(numCols-1, -1, -1): # from numCol-1 to 0
        for r in xrange(numRows-1, -1, -1):    
            if im_bool[r,c] and not isPotentialNoisePoint(im_bool, r, c):
                return (r,c)
    return (None, None)  # client should assert None

def getUppermostCoordinate(im_bool):
    numRows = im_bool.shape[0]
    numCols = im_bool.shape[1]
    for r in xrange(numRows):
        for c in xrange(numCols): 
            if im_bool[r,c] and not isPotentialNoisePoint(im_bool, r, c):
                return (r,c)
    return (None, None)  # client should assert None



def getLowestCoordinate(im_bool):
    numRows = im_bool.shape[0]
    numCols = im_bool.shape[1]
    for r in xrange(numRows-1, -1, -1):     
        for c in xrange(numCols-1, -1, -1): 
            if im_bool[r,c] and not isPotentialNoisePoint(im_bool, r, c):
                return (r,c)
    return (None, None)  # client should assert None

#check if a pixel point is a potential noise point, that is, the 3*3 box around
#it contain "False" value
def isPotentialNoisePoint(im_bool, row, col):
    numRows = im_bool.shape[0]
    numCols = im_bool.shape[1]
    for r in xrange(row - 1, row + 2):
        for c in xrange(col - 1, col + 2):
            if r >= 0 and r < numRows and c >=0 and c < numCols and not im_bool[r,c]:
                return True
    return False
