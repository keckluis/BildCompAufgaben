import cv2 as cv
import time

#code based on OpenCV documentation: https://docs.opencv.org/4.5.5/dc/dbb/tutorial_py_calibration.html

cap = cv.VideoCapture(0)

cv.namedWindow('webcam',  cv.WINDOW_FREERATIO)
print('Press Q to close the window.')
print('Press C to start/stop capturing mode.')
print('Press E to evaluate captured images.')
print('Images confirmed by evaluation will be saved on quit.')
print('WARNING: Existing images will be overwritten.')

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
captured_images = []
calibration_images = []

def captureMode():
    while True:
        ret, frame = cap.read()
        if ret:
            captured_images.append(frame)
            cv.imshow('webcam', frame)

        if cv.waitKey(10) == ord('c'):
            print('Capturing mode stopped.')
            return 
        
        #reduced frame rate to allow repositioning of chessboard
        time.sleep(1)

#finds usable calibration pictures and displays them
def evaluateImages(i):
    print('Evaluating captured images...')

    for img in captured_images:
        #look for chessboard
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        found_cb, corners = cv.findChessboardCorners(img_gray, (7,6), None)

        if found_cb:
            #save confirmed calibration image to separate array
            calibration_images.append(img_gray)

            #show corners for manual verification
            corners2 = cv.cornerSubPix(img_gray, corners, (11,11), (-1,-1), criteria)
            cv.drawChessboardCorners(img, (7,6), corners2, ret)
            cv.imshow('Calibration ' + str(i), img)
            i = i + 1

    print('Found ' + str(len(calibration_images)) + ' calibration images.')
    captured_images = [] #empty array to avoid multiple evaluations of one image

#save calibration image to folder
def saveCalibrationImages():
    j = 0
    for c_img in calibration_images:
        cv.imwrite('Aufgabe1/CalibrationImages/CalibrationImage' + str(j) + '.png', c_img)
        j = j + 1

i = 0 #counter for naming calibration images
#video loop
while True:
    #quit
    if cv.waitKey(3) == ord('q'):
        saveCalibrationImages()
        print('Quit.')
        break

    #capture calibration images
    if cv.waitKey(3) == ord('c'):
        print('Capturing for calibration image...')
        captureMode()

    #find usable calibration images in captured collection
    if cv.waitKey(3) == ord('e'):
        evaluateImages(i)

    #display live image
    ret, frame = cap.read()
    if ret:
        cv.imshow('webcam', frame)
    else:
        print('Camera not found.')

cap.release()
cv.destroyAllWindows()