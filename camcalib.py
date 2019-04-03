import numpy as np
import cv2
import glob

chessSquareDim = 0.01225 #meters

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

objp = objp*chessSquareDim

# Arrays to store object points and image points from all the images.
#objpoints = [] # 3d point in real world space
#imgpoints = [] # 2d points in image plane.

print("camCalib loaded")

#images = glob.glob('./Samples/*.jpg')

#print(cv2.CALIB_CB_ADAPTIVE_THRESH)
#print(cv2.CALIB_CB_NORMALIZE_IMAGE)
#print(cv2.CALIB_CB_FILTER_QUADS)
#print(cv2.CALIB_CB_FAST_CHECK)

#print(images)
def ChessCalib(img,chessSize,chessSquareDim):
    '''
    img - image to analyse
    chessSize - tuple with the chessboard size ie (7,6)
    chessSquareDim - side lenght of a single square meters 
    '''

    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, chessSize,None,cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_NORMALIZE_IMAGE)

    corners2 = None


    # If found, add object points, image points (after refining them)
    if ret == True:
        #objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (7,6), corners2,ret)


    return img,corners2, objp






'''
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)



    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7,6),None,cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_NORMALIZE_IMAGE)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (7,6), corners2,ret)
        cv2.imshow('img',img)
        cv2.waitKey(1)

cv2.destroyAllWindows()



ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)


img = cv2.imread('Samples/left12.jpg')

h,  w = img.shape[:2]

cv2.imshow('imeeg',img)
cv2.waitKey(1)

print(mtx)
newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),0,(w,h))
print(newcameramtx)
print(roi)


# undistort
dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

# crop the image
x,y,w,h = roi
dst = dst[y:y+h, x:x+w]

print(dst.shape)
cv2.imwrite('calibresult4.png',dst)


    
# undistort
dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

# crop the image
x,y,w,h = roi
dst = dst[y:y+h, x:x+w]

print(dst.shape)
cv2.imwrite('calibresult4.png',dst)
    
'''