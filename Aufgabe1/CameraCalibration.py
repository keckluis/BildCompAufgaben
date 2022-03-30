import numpy as np
import cv2 as cv
import glob

#code based on OpenCV documentation: https://docs.opencv.org/4.5.5/dc/dbb/tutorial_py_calibration.html

cap = cv.VideoCapture(0)

#two windows for comparison
cv.namedWindow('webcam original',  cv.WINDOW_FREERATIO)
cv.namedWindow('webcam undistorted',  cv.WINDOW_FREERATIO)
    
#get all images from folder
file_names = [img for img in glob.glob('Aufgabe1/CalibrationImages/*.png')]

#display number of found images, give warning for low number and quit program in case there aren't any
cb_images_count = len(file_names)
if  cb_images_count > 0:
    print('Found ' + str(cb_images_count) + ' calibration images.')
    if cb_images_count < 10:
        print('WARNING: At least 10 images are recommended for camera calibration.')
    print('Press Q to close the window.')   
else:
    print("No calibration image found. Please capture them with 'CaptureCalibrationImages.py' first.")
    cap.release()
    cv.destroyAllWindows()
    quit()

#read images and convert them to needed color space
calibration_images = []
for img in file_names:
    cb_img = cv.imread(img)
    cb_img = cv.cvtColor(cb_img, cv.COLOR_BGR2GRAY)
    calibration_images.append(cb_img)

#calculate camera distortion
objpoints = []
imgpoints = []

objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

for cb_img in calibration_images:
    ret, corners = cv.findChessboardCorners(cb_img, (7, 6), None)
    if ret:
        objpoints.append(objp)
        imgpoints.append(corners)

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, calibration_images[0].shape[::-1], None, None)

h, w = calibration_images[0].shape[:2]
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
    
    #display live image
    ret, frame = cap.read()
    if ret:
        frame_undistorted = removeDistortion(frame)

        #show original and undistorted image for comparison
        cv.imshow('webcam original', frame)
        cv.imshow('webcam undistorted', frame_undistorted)
    else:
        print('Camera not found.')

cap.release()
cv.destroyAllWindows()