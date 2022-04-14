from fileinput import close
import cv2
import numpy as np
import operator

window_name = 'window'
window = cv2.namedWindow(window_name, cv2.WINDOW_FREERATIO)

# load the image
img = cv2.imread('Aufgabe2/table_bottle_01.jpg', cv2.IMREAD_COLOR)
height, width, _ = img.shape

# user instruction
instruction1 = '1. Mark the table corners clockwise or counter-clockwise.'
cv2.putText(img, instruction1, (20, height - 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3, cv2.LINE_8)
print(instruction1)
instruction2 = '2. Mark first the mug and then the bottle height (bottom to top).'
cv2.putText(img, instruction2, (20, height - 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3, cv2.LINE_8)
print(instruction2)

orig_img = img.copy()
cv2.imshow(window_name, img)

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
    cv2.circle(img, intersec_pos, 10, (0, 0, 255), 3)

    # get the points of the 2 lines that are closer to the intersection point
    closer_point1 = getCloserPoint(intersec_pos, clicked_points[a], clicked_points[b])
    closer_point2 = getCloserPoint(intersec_pos, clicked_points[c], clicked_points[d])
    close_points.append(closer_point1)
    close_points.append(closer_point2)

    # draw red lines from the given lines to their vanishing point
    cv2.line(img, closer_point1, intersec_pos, (0, 0, 255), 3)
    cv2.line(img, closer_point2, intersec_pos, (0, 0, 255), 3)

    # add vanishing point in array to monitor progress
    vanishing_points.append(intersec_pos)

# calulates the mug's height based on vanishing points, marked height in image of mug and bottle,
# and known bottle height in centimeters (26cm)
def calculateMugHeight():
    # calculate intersection between vanishing line and line through bottom of mug and bottle
    line1 = getLine(vanishing_points[0], vanishing_points[1])
    line2 = getLine(clicked_points[4], clicked_points[6])
    intersec_pos = getIntersection(line1, line2)
    vanishing_points.append(intersec_pos)

    # draw lines from vanishing line to object bottoms and mug top
    cv2.line(img, clicked_points[4], intersec_pos, (255, 255, 255), 3)
    cv2.line(img, intersec_pos, clicked_points[5], (255, 255, 255), 3)

    # line from vanishing line through mug top
    line3 = getLine(intersec_pos, clicked_points[5])
    # line from bottle bottom to top
    line4 = getLine(clicked_points[6], clicked_points[7])
    # intersection of vertical line on bottle and mug height at bottle position
    mug_top_on_bottle = getIntersection(line3, line4)

    # display mug height at mug and bottle position
    cv2.line(img, clicked_points[6], mug_top_on_bottle, (0, 0, 255), 5)
    cv2.line(img, clicked_points[4], clicked_points[5], (0, 0, 255), 5)
    cv2.circle(img, mug_top_on_bottle, 5, (0, 255, 255), 2)

    # calculate the mug height at bottle position in pixels
    mug_height_px = getDistance(mug_top_on_bottle, clicked_points[6])
    # calculate the bottle height at bottle position in pixels
    bottle_height_px = getDistance(clicked_points[6], clicked_points[7])
    # calculate mug height in centimeters with mug/bottle ratio and known bottle height of 26cm
    mug_height_cm = np.round(((mug_height_px / bottle_height_px) * 26), 2)
    return mug_height_cm

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

    img_points = []
    for i in range(len(close_points)):
        img_points.append(tuple(map(operator.add, close_points[i], origin)))
    img_points.append(tuple(map(operator.add, clicked_points[4], origin)))
    img_points.append(tuple(map(operator.add, clicked_points[5], origin)))
    
    expanded_img[origin[1]:origin[1]+height, origin[0]:origin[0]+width, :] = img

    # draw vanishing line
    cv2.line(expanded_img, v_points_new[0], v_points_new[2], (0, 0, 255), 3)

    # draw lines to vanishing points 
    for i in range(len(v_points_new)):
        cv2.line(expanded_img, v_points_new[i], img_points[i * 2], (255, 255, 255), 3)
        cv2.line(expanded_img, v_points_new[i], img_points[i * 2 + 1], (255, 255, 255), 3)
        cv2.circle(expanded_img, v_points_new[i], 10, (0, 255, 255), -1)

    return expanded_img

global clicked_points
clicked_points = []
global vanishing_points
vanishing_points = []
global close_points
close_points = []
def click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_points.append((x, y))
        
        if len(clicked_points) <= 8:
            cv2.circle(img, (x, y), 5, (0, 255, 255), 2)

        # table corners are marked  
        if len(clicked_points) == 4:
            # vanishing point 1
            calculateVanishingPoints(0, 1, 2, 3, (255, 0, 0))
            # vanishing point 2
            calculateVanishingPoints(0, 3, 1, 2, (0, 255, 0))
        
        # mug and bottle height are marked
        if len(clicked_points) == 8:
            mug_height = str(calculateMugHeight()) + 'cm'

            text_pos = (clicked_points[4][0], clicked_points[4][1] + 100)
            cv2.putText(img, mug_height, text_pos, cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 6, cv2.LINE_8)
            print('Mug height: ' + mug_height)

            expanded_img = expandImage()
            cv2.imshow(window_name, expanded_img)

            cv2.imwrite('Aufgabe2/result.jpg', expanded_img)
            print('Press Q to quit.')

        if len(vanishing_points) < 3:
            cv2.imshow(window_name, img)
            
cv2.setMouseCallback(window_name, click)
while True:
    # quit
    key_press = cv2.waitKey(10)
    if key_press == ord('q'):
        break 
    # clear image
    elif key_press == ord('c'):
        img = orig_img.copy()
        clicked_points = []
        vanishing_points = []
        cv2.imshow(window_name, img)

cv2.destroyAllWindows()