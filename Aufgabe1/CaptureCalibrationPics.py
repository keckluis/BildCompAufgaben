import cv2 as cv

cap = cv.VideoCapture(0)

cv.namedWindow('webcam',  cv.WINDOW_FREERATIO)
print('Press Q to close the window.')
print('Press C to capture a calibration picture.')

def captureFrame(i):
    print('Press X to stop capturing mode.')
    while True:
        ret, frame = cap.read()
        if ret:
            #look for chessboard
            frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            found_cb, corners = cv.findChessboardCorners(frame_gray, (7,6), None)

            #save calibration picture to folder
            if found_cb:
                cv.imwrite('Aufgabe1/CalibrationPics/Calibration' + str(i) + '.png', frame_gray)
                cv.imshow('Calibration ' + str(i), frame_gray)
                print('Calibration picture found.')
                return True

        if cv.waitKey(10) == ord('x'):
            print('Capturing mode stopped.')
            return False

i = 0
#video loop
while True:
    #quit
    if cv.waitKey(10) == ord('q'):
        print('Quit.')
        break

    #capture chessboad image
    if cv.waitKey(10) == ord('c'):
        print('Looking for calibration picture...')
        if captureFrame(i):
            i = i + 1

    #live image
    ret, frame = cap.read()
    if ret:
        cv.imshow('webcam', frame)
    else:
        print('Camera not found.')

cap.release()
cv.destroyAllWindows()