import cv2
import numpy as np

window_name = 'window'
window = cv2.namedWindow(window_name, cv2.WINDOW_FREERATIO)

img = cv2.imread('Aufgabe2/table_bottle_01.jpg', cv2.IMREAD_COLOR)
cv2.imshow(window_name, img)
height, width, _ = img.shape

def getIntersection(line1, line2):
    intersection = np.cross(line1, line2)
    intersection = intersection/intersection[2]
    return (round(intersection[0]), round(intersection[1]))

def getLine(point1, point2):
    point1 = (point1[0], point1[1], 1)
    point2 = (point2[0], point2[1], 1)
    line = np.cross(point1, point2)
    return line

def getDistance(point1, point2):
    point1 = np.array((point1[0], point1[1]))
    point2 = np.array((point2[0], point2[1]))
    return np.linalg.norm(point1 - point2)

def getCloserPoint(intersec_pos, point1, point2): 
    dist1 = getDistance(point1, intersec_pos)
    dist2 = getDistance(point2, intersec_pos)
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
            
        if len(vanishing_points) < 2 and len(clicked_points) == 4:
            cv2.line(img, clicked_points[2], clicked_points[3], (0,255,0), 3) 

            line1 = getLine(clicked_points[0], clicked_points[1])
            line2 = getLine(clicked_points[2], clicked_points[3])
            intersec_pos = getIntersection(line1, line2)
            cv2.circle(img, intersec_pos, 10, (0,0,255), 3)

            closer_point1 = getCloserPoint(intersec_pos, clicked_points[0], clicked_points[1])
            closer_point2 = getCloserPoint(intersec_pos, clicked_points[2], clicked_points[3])
            cv2.line(img, closer_point1, intersec_pos, (0,0,255), 3)
            cv2.line(img, closer_point2, intersec_pos, (0,0,255), 3)
            
            vanishing_points.append(intersec_pos)
            emptyClickedPoints()
        	
        if len(vanishing_points) == 2 and len(clicked_points) == 4:
            line1 = getLine(vanishing_points[0], vanishing_points[1])
            line2 = getLine(clicked_points[0], clicked_points[2])
            intersec_pos = getIntersection(line1, line2)
            vanishing_points.append(intersec_pos)

            cv2.line(img, clicked_points[0], intersec_pos, (150,75,0), 3)
            cv2.line(img, clicked_points[2], intersec_pos, (150,75,0), 3)
            cv2.line(img, vanishing_points[2], clicked_points[1], (150,75,0), 3)

            line3 = getLine(intersec_pos, clicked_points[1])
            line4 = getLine(clicked_points[2], clicked_points[3])
            mug_top_on_bottle = getIntersection(line3, line4)
            cv2.circle(img, mug_top_on_bottle, 2, (0,255,255), 5)
            
            mug_height_px = getDistance(mug_top_on_bottle, clicked_points[2])
            bottle_height_px = getDistance(clicked_points[2], clicked_points[3])
            mug_height_cm = np.round(((mug_height_px / bottle_height_px) * 26), 2)
            print(mug_height_cm)

        cv2.imshow(window_name, img)
            
cv2.setMouseCallback(window_name, click)
while True:
    if cv2.waitKey(10) == ord('q'):
        break 
cv2.destroyAllWindows()