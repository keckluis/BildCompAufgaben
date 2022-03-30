import numpy as np
import cv2 as cv

#code based on OpenCV documentation: https://docs.opencv.org/4.5.5/dc/dbb/tutorial_py_calibration.html

cap = cv.VideoCapture(0)

#window names
window_original = 'webcam original'
window_undistorted = 'webcam undistorted'

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

#get file with calibration data
file_name = input('Please enter the name of your calibration file >')
calibration_data = np.load('Aufgabe1/' + file_name + '.npz')
obj_points = calibration_data['obj_points']
img_points = calibration_data['img_points']

#quit if file is not usable
cal_images = len(obj_points)
if cal_images == 0:
    print('Invalid calibration data. Please try a different file.')
    cap.release()
    cv.destroyAllWindows()
    quit()
else:
    print('Found data of ' + str(cal_images) + ' calibration images.')


ref_img = cv.imread('Aufgabe1/ref_img.png')
ref_img = cv.cvtColor(ref_img, cv.COLOR_BGR2GRAY)
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(obj_points, img_points, ref_img.shape[::-1], None, None)

h, w = ref_img.shape[:2]
new_camera_matrix, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

#remove distortion of current frame
def removeDistortion(frame):
    frame = cv.undistort(frame, mtx, dist, None, new_camera_matrix)
    x, y, w, h = roi
    frame = frame[y:y+h, x:x+w]
    return frame

#two windows for comparison
cv.namedWindow(window_original,  cv.WINDOW_FREERATIO)
cv.namedWindow(window_undistorted,  cv.WINDOW_FREERATIO)

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
        cv.imshow(window_original, frame)
        cv.imshow(window_undistorted, frame_undistorted)
    else:
        print('Camera not found.')

cap.release()
cv.destroyAllWindows()