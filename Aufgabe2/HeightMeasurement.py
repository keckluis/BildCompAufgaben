import cv2
import numpy as np

window_name = 'window'
window = cv2.namedWindow(window_name, cv2.WINDOW_FREERATIO)

img = cv2.imread('Aufgabe2/table_bottle_01.jpg', cv2.IMREAD_COLOR)
height, width, _ = img.shape

def getIntersectionPosition(line1, line2):
    intersection = np.cross(line1, line2)
    intersection = intersection/intersection[2]
    return (round(intersection[0]), round(intersection[1]))

def getLines(clicked_points):
    point1 = (clicked_points[0][0], clicked_points[0][1], 1)
    point2 = (clicked_points[1][0], clicked_points[1][1], 1)
    line1 = np.cross(point1, point2)

    point3 = (clicked_points[2][0], clicked_points[2][1], 1)
    point4 = (clicked_points[3][0], clicked_points[3][1], 1)
    line2 = np.cross(point3, point4)

    return line1, line2

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

global clicked_points
clicked_points = []
def click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_points.append((x,y))

        cv2.circle(img, (x, y), 2, (0,255,255), 5)
        if len(clicked_points) == 2:
            cv2.line(img, clicked_points[0], clicked_points[1], (255,0,0), 3)
            
        if len(clicked_points) == 4:
            cv2.line(img, clicked_points[2], clicked_points[3], (0,255,0), 3) 

            line1, line2 = getLines(clicked_points)
            intersec_pos = getIntersectionPosition(line1, line2)
            cv2.circle(img, intersec_pos, 10, (0,0,255), 3)

            closer_point1 = getCloserPoint(intersec_pos, clicked_points[0], clicked_points[1])
            closer_point2 = getCloserPoint(intersec_pos, clicked_points[2], clicked_points[3])
            cv2.line(img, closer_point1, intersec_pos, (0,0,255), 3)
            cv2.line(img, closer_point2, intersec_pos, (0,0,255), 3)
             
            print('Intersection at: ' + str(intersec_pos))
        	
            while len(clicked_points) != 0:
                clicked_points.pop()

        cv2.imshow(window_name, img)
            
cv2.setMouseCallback(window_name, click)
while True:
    cv2.imshow(window_name, img)
    if cv2.waitKey(10) == ord('q'):
        break
cv2.destroyAllWindows()