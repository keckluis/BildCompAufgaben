import cv2 as cv
import numpy as np
import time

# code based on OpenCV documentation: https://docs.opencv.org/4.5.5/dc/dbb/tutorial_py_calibration.html
# code from documentation is marked with 'OpenCV'

# user instructions
print('Press Q to quit.')
print('Press C to start/stop capturing mode.')
print('Press E to evaluate captured images.')
print('Data confirmed by evaluation will be saved on quit.')

cap = cv.VideoCapture(0)

# window names
window_calibration = 'calibration picture'
window_webcam = 'webcam'

cv.namedWindow(window_webcam,  cv.WINDOW_FREERATIO)

# OpenCV: needed for displaying corners in calibration images
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# to save captured and 'chosen for calibration' images
captured_images = []
calibration_images = []

# saves one image per second for capturing calibration images
def captureMode(captured_images):
    while True:
        ret, frame = cap.read()
        if ret:
            # save current frame
            captured_images.append(frame)
            cv.imshow(window_webcam, frame)
    	
        # quit capture mode
        if cv.waitKey(10) == ord('c'):
            print('Capturing mode stopped.')
            return 
        
        # reduced frame rate to allow repositioning of chessboard
        time.sleep(1)

# finds usable calibration images and displays them 
# user can choose to save or delete individual images
def evaluateImages(calibration_images, captured_images):  
    # user instructions  
    print('Evaluating captured images...')
    print('S: save image, D: delete image')

    cv.namedWindow(window_calibration, cv.WINDOW_FREERATIO)

    for img in captured_images:
        # OpenCV: look for chessboard in image
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        found_cb, corners = cv.findChessboardCorners(img_gray, (7,6), None)

        if found_cb:
            # OpenCV: show corners for manual verification
            corners2 = cv.cornerSubPix(img_gray, corners, (11,11), (-1,-1), criteria)
            cv.drawChessboardCorners(img, (7,6), corners2, ret)
            cv.imshow('calibration picture', img)

            # save confirmed calibration image to separate array
            while True:
                key_press = cv.waitKey(10)
                if key_press == ord('s'):
                    calibration_images.append(img_gray)
                    break
                elif key_press == ord('d'):
                    break

    print('Saved ' + str(len(calibration_images)) + ' calibration images.')

    # empty array to avoid multiple evaluations of one image

    captured_images = []
    cv.destroyWindow(window_calibration)
    return calibration_images, captured_images

# save calibration data as arrays
def saveCalibrationData(calibration_images):
    # OpenCV: calculate calibration data based on chosen images
    obj_points = []
    img_points = []

    obj_p = np.zeros((6*7,3), np.float32)
    obj_p[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

    for cb_img in calibration_images:
        ret, corners = cv.findChessboardCorners(cb_img, (7, 6), None)
        if ret:
            obj_points.append(obj_p)
            img_points.append(corners)
    
    # saves calibration data in file named by user input in console
    file_name = input('Enter a file name for your calibration data (without format) >')
    np.savez('Aufgabe1/' + file_name + '.npz', obj_points=obj_points, img_points=img_points)
    
# video loop
while True:
    key_press = cv.waitKey(10)
    
    # capture calibration images
    if key_press == ord('c'):
        print('Capturing calibration image...')
        captureMode(captured_images)

    # find usable calibration images in captured collection
    elif key_press == ord('e'):
        calibration_images, captured_images = evaluateImages(calibration_images, captured_images)
    
    # quit
    elif key_press == ord('q'):
        saveCalibrationData(calibration_images)
        print('Quit.')
        break

    # display live image
    ret, frame = cap.read()
    if ret:
        cv.imshow(window_webcam, frame)
    else:
        print('Camera not found.')

cap.release()
cv.destroyAllWindows()