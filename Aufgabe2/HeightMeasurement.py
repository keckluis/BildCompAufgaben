import cv2
import numpy as np

window_name = 'window'
window = cv2.namedWindow(window_name, cv2.WINDOW_FREERATIO)

img = cv2.imread('Aufgabe2/table_bottle_01.jpg', cv2.IMREAD_COLOR)
orig_img = img.copy()
height, width, _ = img.shape

def getIntersectionPosition(line1, line2):
    intersection = np.cross(line1, line2)
    intersection = intersection/intersection[2]
    return (round(intersection[0]), round(intersection[1]))

def getLine(point1, point2):
    point1 = (point1[0], point1[1], 1)
    point2 = (point2[0], point2[1], 1)
    line = np.cross(point1, point2)
    return line

def getCloserPoint(intersec_pos, point1, point2):
    intersec_pos = np.array((intersec_pos[0], intersec_pos[1]))
    p1 = np.array((point1[0], point1[1]))
    p2 = np.array((point2[0], point2[1]))
    dist1 = np.linalg.norm(p1 - intersec_pos)
    dist2 = np.linalg.norm(p2 - intersec_pos)
    if dist1 <= dist2:
        return point1
    else:
        return point2

def emptyClickedPoints():
    while len(clicked_points) != 0:
        clicked_points.pop()

global clicked_points
clicked_points = []
global vanishing_points
vanishing_points = []
def click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_points.append((x,y))

        cv2.circle(img, (x, y), 2, (0,255,255), 5)
        if len(vanishing_points) < 2 and len(clicked_points) == 2:
            cv2.line(img, clicked_points[0], clicked_points[1], (255,0,0), 3)
            
        if len(clicked_points) == 4:
            cv2.line(img, clicked_points[2], clicked_points[3], (0,255,0), 3) 

            line1 = getLine(clicked_points[0], clicked_points[1])
            line2 = getLine(clicked_points[2], clicked_points[3])
            intersec_pos = getIntersectionPosition(line1, line2)
            cv2.circle(img, intersec_pos, 10, (0,0,255), 3)

            closer_point1 = getCloserPoint(intersec_pos, clicked_points[0], clicked_points[1])
            closer_point2 = getCloserPoint(intersec_pos, clicked_points[2], clicked_points[3])
            cv2.line(img, closer_point1, intersec_pos, (0,0,255), 3)
            cv2.line(img, closer_point2, intersec_pos, (0,0,255), 3)
            
            vanishing_points.append(intersec_pos)
            print('Intersection at: ' + str(intersec_pos))
            emptyClickedPoints()
        	
        if len(vanishing_points) == 2 and len(clicked_points) == 2:
            line1 = getLine(vanishing_points[0], vanishing_points[1])
            line2 = getLine(clicked_points[0], clicked_points[1])
            intersec_pos = getIntersectionPosition(line1, line2)
            vanishing_points.append(intersec_pos)
            closer_point = getCloserPoint(intersec_pos, clicked_points[0], clicked_points[1])
            cv2.line(img, closer_point, intersec_pos, (150,75,0), 3)

        if len(vanishing_points) == 3 and len(clicked_points) == 3:
            cv2.line(img, vanishing_points[2], clicked_points[2], (150,75,0), 3)
            emptyClickedPoints()

        cv2.imshow(window_name, img)
            
cv2.setMouseCallback(window_name, click)
while True:
    cv2.imshow(window_name, img)

    key_press = cv2.waitKey(10)
    if key_press == ord('q'):
        break
    elif key_press == ord('c'):
        img = orig_img.copy()
        cv2.imshow(window_name, img)
        emptyClickedPoints()

cv2.destroyAllWindows()