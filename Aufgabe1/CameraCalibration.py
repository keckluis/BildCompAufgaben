from cgi import test
import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)
width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
print('width: ' + str(width) + ', height: ' + str(height))

cv.namedWindow('webcam',  cv.WINDOW_FREERATIO)
print('Press Q to close the window.')

def showLiveImage():
    ret, frame = cap.read()
    if ret:
        cv.imshow('webcam', frame)
        return frame
    else:
        print('Camera not found.')

def captureFrame():
    while True:
        ret, current_frame = cap.read()
        if ret:
            print('Test frame captured.')
            return current_frame    

test_frames = []
while True:
    if cv.waitKey(10) == ord('q'):
        break
    if cv.waitKey(10) == ord('c'):
        test_frames.append(captureFrame())
    if cv.waitKey(10) == ord('s'):
        i = 0
        for ts in test_frames:
            cv.imshow('test frame ' + str(i), ts)
            i = i+1
    showLiveImage()

cap.release()
cv.destroyAllWindows()

#TODO: read at least 10 frames with chessboard image (live or prepared?)

#TODO: calculate distortion of camera based on chessboard images

#TODO: remove distortion from each frame in live video feed

#TODO: compute reprojection error for one image (mm)