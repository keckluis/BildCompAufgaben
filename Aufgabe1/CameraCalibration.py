#import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
print('width: ' + str(width) + ', height: ' + str(height))

cv.namedWindow('webcam',  cv.WINDOW_FREERATIO)
print('Press q to close the window.')

while True:
    ret, frame = cap.read()
    if (ret):
        cv.imshow('webcam', frame)

        if cv.waitKey(10) == ord('q'):
            break
    else:
        print('camera frame read unsuccessful.')
        break

cap.release()
cv.destroyAllWindows()