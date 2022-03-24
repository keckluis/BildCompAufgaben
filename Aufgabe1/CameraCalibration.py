import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
print('width: ' + str(width) + ', height: ' + str(height))

cv.namedWindow('webcam',  cv.WINDOW_FREERATIO)
print('Press Q to close the window.')

objpoints = [] 
imgpoints = []

objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

def readChessboard(frame):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    ret, corners = cv.findChessboardCorners(gray, (7, 6), None)

    if ret  == True:
        objpoints.append(objp)

        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners)

        cv.drawChessboardCorners(frame, (7,6), corners2, ret)
        cv.imshow('result', frame)

        print('Camera distortion calculated.')
        return True, gray

    return False, gray

def undistort(frame, gray):
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    h,  w = frame.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    dst = cv.undistort(frame, mtx, dist, None, newcameramtx)
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    frame = dst
    return frame

distortionKnown = False
while True:
    ret, frame = cap.read()
    if ret:            

        if cv.waitKey(10) == ord('q'):
            break

        if distortionKnown:
            frame = undistort(frame, gray)
        else:
            distortionKnown, gray = readChessboard(frame)

        cv.imshow('webcam', frame)
        
    else:
        print('Camera not found.')
        break

cap.release()
cv.destroyAllWindows()