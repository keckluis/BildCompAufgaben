import numpy as np
import cv2 as cv

# code based on OpenCV documentation: https://docs.opencv.org/4.5.5/dc/dbb/tutorial_py_calibration.html
# code from documentation is marked with 'OpenCV'

# user instructions
print('Press Q to quit.')

cap = cv.VideoCapture(0)

# window names
window_original = 'webcam original'
window_undistorted = 'webcam undistorted'

# get file with calibration data
file_name = input('Enter the name of your calibration file (without format) >')

# try to load file and ask for new input if not found
while True:
    try:
        calibration_data = np.load(file_name + '.npz')
        break
    except:
        file_name = input('File not found. Try again >')

obj_points = calibration_data['obj_points']
img_points = calibration_data['img_points']

# quit if file is not usable
cal_images = len(obj_points)
if cal_images == 0:
    print('Invalid calibration data. Try a different file.')
    cap.release()
    cv.destroyAllWindows()
    quit()
else:
    print('Found data of ' + str(cal_images) + ' calibration images.')

# get camera frame for size reference
ret, ref_frame = cap.read()
if ret:
    ref_img = cv.cvtColor(ref_frame, cv.COLOR_BGR2GRAY)
else:
    print('Camera not found.')
    quit()

# OpenCV: calibrate camera based on calibration data
ret, intrinsic_mtx, dist_coeffs, rotation_vecs, translation_vecs = cv.calibrateCamera(obj_points, img_points, ref_img.shape[::-1], None, None)

# OpenCV: calculate new camera matrix to remove distortion of a frame
h, w = ref_img.shape[:2]
new_camera_matrix, roi = cv.getOptimalNewCameraMatrix(intrinsic_mtx, dist_coeffs, (w, h), 1, (w, h))

# OpenCV: remove distortion of current frame
def removeDistortion(frame):
    frame_undistorted = cv.undistort(frame, intrinsic_mtx, dist_coeffs, None, new_camera_matrix)
    x, y, w, h = roi
    frame_undistorted = frame_undistorted[y:y+h, x:x+w]
    return frame_undistorted

# two windows for comparison
cv.namedWindow(window_original, cv.WINDOW_FREERATIO)
cv.namedWindow(window_undistorted, cv.WINDOW_FREERATIO)

# video loop
while True:
    #quit
    if cv.waitKey(10) == ord('q'):
        print('Quit.')
        break
    
    # display live image
    ret, frame = cap.read()
    if ret:
        frame_undistorted = removeDistortion(frame)

        # show original and undistorted image for comparison
        cv.imshow(window_original, frame)
        cv.imshow(window_undistorted, frame_undistorted)
    else:
        print('Camera not found.')
        break

cap.release()
cv.destroyAllWindows()