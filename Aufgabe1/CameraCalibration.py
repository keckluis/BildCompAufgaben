import numpy as np
import cv2 as cv
import glob

cap = cv.VideoCapture(0)

cv.namedWindow('webcam',  cv.WINDOW_FREERATIO)
    
#read all images in folder
file_names = [img for img in glob.glob('Aufgabe1/CalibrationPics/*.png')]

cb_pics_count = len(file_names)
if  cb_pics_count > 0:
    print('Found ' + str(cb_pics_count) + ' calibration pictures.')
    if cb_pics_count < 10:
        print('WARNING: At least 10 pictures are recommended for camera calibration.')
    print('Press Q to close the window.')   
else:
    print("No calibration pictures found. Please capture them with 'CaptureCalibrationPics.py' first.")
    cap.release()
    cv.destroyAllWindows()
    quit()

calibration_pics = []
for img in file_names:
    cb_pic = cv.imread(img)
    cb_pic = cv.cvtColor(cb_pic, cv.COLOR_BGR2GRAY)
    calibration_pics.append(cb_pic)

#calculate distortion
objpoints = []
imgpoints = []

objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

for cb_pic in calibration_pics:
    ret, corners = cv.findChessboardCorners(cb_pic, (7, 6), None)
    if ret:
        objpoints.append(objp)
        imgpoints.append(corners)

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, calibration_pics[0].shape[::-1], None, None)

h, w = calibration_pics[0].shape[:2]
new_camera_matrix, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

#remove distortion of current frame
def removeDistortion(frame):
    frame = cv.undistort(frame, mtx, dist, None, new_camera_matrix)
    x, y, w, h = roi
    frame = frame[y:y+h, x:x+w]
    return frame
      
#video loop
while True:
    #quit
    if cv.waitKey(10) == ord('q'):
        print('Quit.')
        break
    
    #live image
    ret, frame = cap.read()
    if ret:
        frame = removeDistortion(frame)
        cv.imshow('webcam', frame)
    else:
        print('Camera not found.')

cap.release()
cv.destroyAllWindows()