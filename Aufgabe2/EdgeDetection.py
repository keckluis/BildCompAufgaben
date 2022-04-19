import cv2
import numpy as np

window_name = 'window'
window = cv2.namedWindow(window_name, cv2.WINDOW_FREERATIO)

img = cv2.imread('Aufgabe2/table_bottle_01.jpg', cv2.IMREAD_COLOR)
edges = cv2.Canny(img, 50, 200)

# https://stackoverflow.com/questions/57535865/extract-vanishing-point-from-lines-with-open-cv
lines = cv2.HoughLines(edges, 0.7, np.pi / 120, 120, min_theta=np.pi / 36, max_theta=np.pi-np.pi / 36)
for line in lines:
    rho,theta = line[0]
    # skip near-vertical lines
    if abs(theta-np.pi / 90) < np.pi / 9:
        continue 
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 10_000 * -b)
    y1 = int(y0 + 10_000 * a)
    x2 = int(x0 - 10_000 * -b)
    y2 = int(y0 - 10_000 * a)
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 0), 2)

cv2.imshow(window_name, img)
while True:
    key_press = cv2.waitKey(10)
    if key_press == ord('q'):
        break 
cv2.destroyAllWindows()
