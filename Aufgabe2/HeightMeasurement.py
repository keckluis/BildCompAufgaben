import cv2
import numpy as np

# user instruction
print('Mark the table corners clockwise or counter-clockwise.')
window_name = 'window'
window = cv2.namedWindow(window_name, cv2.WINDOW_FREERATIO)

# load the image
img = cv2.imread('Aufgabe2/table_bottle_01.jpg', cv2.IMREAD_COLOR)
cv2.imshow(window_name, img)
height, width, _ = img.shape

# returns position of intersection of 2 lines
def getIntersection(line1, line2):
    intersection = np.cross(line1, line2)
    intersection = intersection/intersection[2]
    return (round(intersection[0]), round(intersection[1]))

# returns a line through two points
def getLine(point1, point2):
    point1 = (point1[0], point1[1], 1)
    point2 = (point2[0], point2[1], 1)
    line = np.cross(point1, point2)
    return line

# returns the distance of 2 points
def getDistance(point1, point2):
    point1 = np.array((point1[0], point1[1]))
    point2 = np.array((point2[0], point2[1]))
    return np.linalg.norm(point1 - point2)

# returns the point that is closer to the 'compared_to' point
def getCloserPoint(compared_to, point1, point2): 
    dist1 = getDistance(point1, compared_to)
    dist2 = getDistance(point2, compared_to)
    if dist1 <= dist2:
        return point1
    else:
        return point2

# takes 4 points to form 2 lines (ab and cd) and calculates their intersection (vanishing point)
def calculateVanishingPoints(a, b, c, d, color):
    # calculate the intersection
    line1 = getLine(clicked_points[a], clicked_points[b])
    line2 = getLine(clicked_points[c], clicked_points[d])
    intersec_pos = getIntersection(line1, line2)

    # draw the two given lines
    cv2.line(img, clicked_points[a], clicked_points[b], color, 3)
    cv2.line(img, clicked_points[c], clicked_points[d], color, 3) 

    # draw a circle at intersection position
    cv2.circle(img, intersec_pos, 10, (0,0,255), 3)

    # get the points of the 2 lines that are closer to the intersection point
    closer_point1 = getCloserPoint(intersec_pos, clicked_points[a], clicked_points[b])
    closer_point2 = getCloserPoint(intersec_pos, clicked_points[c], clicked_points[d])

    # draw red lines from the given lines to their vanishing point
    cv2.line(img, closer_point1, intersec_pos, (0,0,255), 3)
    cv2.line(img, closer_point2, intersec_pos, (0,0,255), 3)

    # add vanishing point in array to monitor progress
    vanishing_points.append(intersec_pos)

# calulates the mug's height based on vanishing points, marked height in image of mug and bottle,
# and known bottle height in centimeters (26cm)
def calculateMugHeight():
    # calculate intersection between vanishing line and line through bottom of mug and bottle
    line1 = getLine(vanishing_points[0], vanishing_points[1])
    line2 = getLine(clicked_points[0], clicked_points[2])
    intersec_pos = getIntersection(line1, line2)

    # draw lines from vanishing line to object bottoms and mug top
    cv2.line(img, clicked_points[0], intersec_pos, (150,75,0), 3)
    cv2.line(img, intersec_pos, clicked_points[1], (150,75,0), 3)

    # line from vanishing line through mug top
    line3 = getLine(intersec_pos, clicked_points[1])
    # line from bottle bottom to top
    line4 = getLine(clicked_points[2], clicked_points[3])
    # intersection of vertical line on bottle and mug height at bottle position
    mug_top_on_bottle = getIntersection(line3, line4)
    # display mug height at bottle position
    cv2.circle(img, mug_top_on_bottle, 2, (0,255,255), 5)
    
    # calculate the mug height at bottle position in pixels
    mug_height_px = getDistance(mug_top_on_bottle, clicked_points[2])
    # calculate the bottle height at bottle position in pixels
    bottle_height_px = getDistance(clicked_points[2], clicked_points[3])
    # calculate mug height in centimeters with mug/bottle ratio and known bottle height of 26cm
    mug_height_cm = np.round(((mug_height_px / bottle_height_px) * 26), 2)
    return mug_height_cm

# clear the clicked points for next step
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

        # table corners are marked  
        if len(vanishing_points) < 2 and len(clicked_points) == 4:
            # vanishing point 1
            calculateVanishingPoints(0, 1, 2, 3, (255,0,0))
            # vanishing point 2
            calculateVanishingPoints(0, 3, 1, 2, (0,255,0))
            emptyClickedPoints()
            print('Mark first the mug and then the bottle height (bottom to top).')
        
        # mug and bottle height are marked
        if len(vanishing_points) == 2 and len(clicked_points) == 4:
            print('Mug height: ' + str(calculateMugHeight()) + 'cm')
            print('Press Q to quit.')

        cv2.imshow(window_name, img)
            
cv2.setMouseCallback(window_name, click)
while True:
    # quit
    if cv2.waitKey(10) == ord('q'):
        break 
cv2.destroyAllWindows()