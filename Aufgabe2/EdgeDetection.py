import cv2
import numpy as np
import operator

window_name = 'window'
window = cv2.namedWindow(window_name, cv2.WINDOW_FREERATIO)

img = cv2.imread('Aufgabe2/table_bottle_01.jpg', cv2.IMREAD_COLOR)
height, width, _ = img.shape

edges = cv2.Canny(img, 50, 200)

# returns a line through two points
def getLine(point1, point2):
    point1 = (point1[0], point1[1], 1)
    point2 = (point2[0], point2[1], 1)
    line = np.cross(point1, point2)
    return line

# returns position of intersection of 2 lines
def getIntersection(line1, line2):
    intersection = np.cross(line1, line2)
    intersection = intersection/intersection[2]
    return (round(intersection[0]), round(intersection[1]))

# expand image to show vanishing line
# based on BC_tutorial_09
def expandImage():
    min_x = min(min(vanishing_points)[0], 0)
    max_x = max(max(vanishing_points)[0], width)
    min_y = min(min(vanishing_points, key=lambda x: x[1])[1], 0)
    max_y = max(max(vanishing_points, key=lambda x: x[1])[1], height)
    border = 50  # pixel border so that vanishing points are fully visible
    expanded_width = max_x - min_x + (border * 2)
    expanded_height = max_y - min_y + (border * 2)
    expanded_img = np.zeros((expanded_height, expanded_width, 3), np.uint8)

    # get original image region and vanishing points in world_img coordinates
    # world image is translated about min_world + border
    origin = (abs(min_x) + border, abs(min_y) + border)

    v_points_new = []
    for i in range(len(vanishing_points)):
        v_points_new.append(tuple(map(operator.add, vanishing_points[i], origin)))

    expanded_img[origin[1]:origin[1]+height, origin[0]:origin[0]+width, :] = img

    # draw vanishing line
    cv2.line(expanded_img, v_points_new[0], v_points_new[len(v_points_new) - 1], (0, 0, 255), 3)

    return expanded_img


# https://stackoverflow.com/questions/57535865/extract-vanishing-point-from-lines-with-open-cv
found_lines = cv2.HoughLines(edges, 0.7, np.pi / 120, 120, min_theta=np.pi / 36, max_theta=np.pi-np.pi / 36)
lines = []
for line in found_lines:
    rho, theta = line[0]
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
    point1 = (x1, y1)
    point2 = (x2, y2)
    lines.append((point1, point2))

rising_lines = []
falling_lines = []
for line in lines:
    if (line[0][0] < line[1][0]):
        rising_lines.append(getLine(line[0], line[1]))
    else:
        falling_lines.append(getLine(line[0], line[1]))

global vanishing_points
vanishing_points = []
for i in range(len(rising_lines) - 1):
    vanishing_points.append(getIntersection(rising_lines[i], rising_lines[i + 1]))
for i in range(len(falling_lines) - 1):
    vanishing_points.append(getIntersection(falling_lines[i], falling_lines[i + 1]))

img = expandImage()

cv2.imshow(window_name, img)
while True:
    key_press = cv2.waitKey(10)
    if key_press == ord('q'):
        break 
cv2.destroyAllWindows()
