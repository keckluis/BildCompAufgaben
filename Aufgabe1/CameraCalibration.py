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

def captureFrames():
    capture_frames = []
    for i in range(15):
        print('Reading frame ' + str(i))
        ret, current_frame = cap.read()
        if ret: 
            capture_frames.append(current_frame)
            cv.imshow('test' + str(i), current_frame)
    return capture_frames

while True:
    
    if cv.waitKey(10) == ord('q'):
        break
    if cv.waitKey(10) == ord('c'):
        frames = captureFrames()

    showLiveImage()

cap.release()
cv.destroyAllWindows()

#TODO: read at least 10 frames with chessboard image (live or prepared?)

#TODO: calculate distortion of camera based on chessboard images

#TODO: remove distortion from each frame in live video feed

#TODO: compute reprojection error for one image (mm)