# Code adapted from:
# docs.opencv2.org/4.5.5/da/de9/tutorial_py_epipolar_geometry.html
# www.andreasjakl.com/understand-and-apply-stereo-rectification-for-depth-maps-part-2/
import cv2
import numpy as np


def findKeypoints(_img1, _img2):
    # Find the keypoints and descriptors using SIFT_create.
    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(_img1, None)
    kp2, des2 = sift.detectAndCompute(_img2, None)
    print('We found %d keypoints in the left image.' % len(kp1))
    print('We found %d keypoints in the right image.' % len(kp2))
    print('Each SIFT keypoint is described with a %s-d array' % des1.shape[1])

    # Visualize the SIFT keypoints.
    img_sift1 = cv2.drawKeypoints(
        _img1, kp1, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    img_sift2 = cv2.drawKeypoints(
        _img2, kp2, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    cv2.imshow(title, np.concatenate((img_sift1, img_sift2), axis=1))
    cv2.waitKey(0)

    return kp1, kp2, des1, des2


# Match the keypoints using a FlannBasedMatcher.
def matchKeypoints(_kp1, _kp2, _des1, _des2):
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(_des1, _des2, k=2)
    matchesMask = [[0, 0] for i in range(len(matches))]
    pts1 = []
    pts2 = []

    # Ratio test as per Lowe's paper.
    # Only use matches with a reasonable small distance.
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.8 * n.distance:
            matchesMask[i] = [1, 0]
            pts1.append(_kp1[m.queryIdx].pt)
            pts2.append(_kp2[m.trainIdx].pt)

    return pts1, pts2


def findFundamentalMatrix(_pts1, _pts2):
    pts1 = np.int32(_pts1)
    pts2 = np.int32(_pts2)
    assert(len(pts1) == len(pts2))
    print('Found %d matching keypoints in both images.' % len(pts1))

    # Compute the fundamental matrix.
    F, mask = cv2.findFundamentalMat(pts1, pts2, cv2.FM_RANSAC)
    print('\nFundamental matrix\n', '\n'.join(['\t'.join(
        ['%03.4f' % cell for cell in row]) for row in F]))

    # Select only inlier points.
    pts1 = pts1[mask.ravel() == 1]
    pts2 = pts2[mask.ravel() == 1]

    return pts1, pts2, F


def findEpilines(_img1, _img2, _pts1, _pts2, _F):
    # Find epilines corresponding to points in right image (second image) and
    # draw its lines on left image.
    lines1 = cv2.computeCorrespondEpilines(_pts2.reshape(-1, 1, 2), 2, _F)
    lines1 = lines1.reshape(-1, 3)
    e_lines1 = drawEpilines(_img1, _img2, lines1, _pts1, _pts2)

    # Find epilines corresponding to points in left image (first image) and
    # draw its lines on right image.
    lines2 = cv2.computeCorrespondEpilines(_pts1.reshape(-1, 1, 2), 1, _F)
    lines2 = lines2.reshape(-1, 3)
    e_lines2 = drawEpilines(_img2, _img1, lines2, _pts2, _pts1)
    cv2.imshow(title, np.concatenate((e_lines2, e_lines1), axis=1))
    cv2.waitKey(0)


# Draw epilines.
def drawEpilines(_img1, _img2, _lines, _pts1, _pts2):
    r, c = _img1.shape
    _img1 = cv2.cvtColor(_img1, cv2.COLOR_GRAY2BGR)
    _img2 = cv2.cvtColor(_img2, cv2.COLOR_GRAY2BGR)
    for r, pt1, pt2 in zip(_lines, _pts1, _pts2):
        color = tuple(np.random.randint(0, 255, 3).tolist())
        x0, y0 = map(int, [0, -r[2] / r[1]])
        x1, y1 = map(int, [c, -(r[2] + r[0] * c) / r[1]])
        _img1 = cv2.line(_img1, (x0, y0), (x1, y1), color, 1)
        _img1 = cv2.circle(_img1, tuple(pt1), 2, color, -1)
        _img2 = cv2.circle(_img2, tuple(pt2), 2, color, -1)
    return _img1


def rectifyImages(_img1, _img2, _pts1, _pts2, _F):
    h1, w1 = _img1.shape
    h2, w2 = _img2.shape
    _, H1, H2 = cv2.stereoRectifyUncalibrated(
        np.float32(_pts1),
        np.float32(_pts2),
        _F,
        imgSize=(w1, h1)
    )

    img1_rectified = cv2.warpPerspective(_img1, H1, (w1, h1))
    img2_rectified = cv2.warpPerspective(_img2, H2, (w2, h2))
    cv2.imshow(title, np.concatenate((img1_rectified, img2_rectified), axis=1))
    cv2.waitKey(0)
    return img1_rectified, img2_rectified


def createDepthMap(_img1_rectified, _img2_rectified):
    # Matched block size. It must be an odd number >=1.
    # Normally, it should be somewhere in the 3..11 range.
    block_size = 11

    # Maximum disparity minus minimum disparity.
    # The value is always greater than zero.
    # In the current implementation, this parameter must be divisible by 16.
    min_disp = -64
    max_disp = 128
    num_disp = max_disp - min_disp

    # Margin in percentage by which the best computed cost function value
    # should "win" the second best value to consider the found match correct.
    # Normally, a value within the 5-15 range is good enough.
    uniqueness_ratio = 5

    # Maximum size of smooth disparity regions to consider their noise
    # speckles and invalidate.
    # Set it to 0 to disable speckle filtering.
    # Otherwise, set it somewhere in the 50-200 range.
    speckle_window_size = 200

    # Maximum disparity variation within each connected component.
    # If you do speckle filtering, set the parameter to a positive value,
    # it will be implicitly multiplied by 16.
    # Normally, 1 or 2 is good enough.
    speckle_range = 4
    disp12_max_diff = 0

    stereo = cv2.StereoSGBM_create(
        minDisparity=min_disp,
        numDisparities=num_disp,
        blockSize=block_size,
        uniquenessRatio=uniqueness_ratio,
        speckleWindowSize=speckle_window_size,
        speckleRange=speckle_range,
        disp12MaxDiff=disp12_max_diff,
        P1=8 * 1 * block_size * block_size,
        P2=32 * 1 * block_size * block_size,
    )
    disparity_SGBM = stereo.compute(_img1_rectified, _img2_rectified)

    # Normalize the values to a range from 0..255 for a grayscale image.
    disparity_SGBM = cv2.normalize(
        disparity_SGBM,
        disparity_SGBM,
        alpha=255,
        beta=0,
        norm_type=cv2.NORM_MINMAX
    )

    depth_map = np.uint8(disparity_SGBM)
    cv2.imshow(title, depth_map)
    cv2.waitKey(0)
    return depth_map


# Calls all needed functions to create depth map based on 2 images.
def getDepthMap(_img1, _img2):
    kp1, kp2, des1, des2 = findKeypoints(_img1, _img2)
    pts1, pts2 = matchKeypoints(kp1, kp2, des1, des2)
    pts1, pts2, F = findFundamentalMatrix(pts1, pts2)
    findEpilines(img1, img2, pts1, pts2, F)
    img1_rectified, img2_rectified = rectifyImages(_img1, _img2, pts1, pts2, F)
    return createDepthMap(img1_rectified, img2_rectified)


# Load images.
img1 = cv2.imread('Aufgabe3/img/dva1_half_res.jpg', cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('Aufgabe3/img/dva2_half_res.jpg', cv2.IMREAD_GRAYSCALE)
img3 = cv2.imread('Aufgabe3/img/dva3_half_res.jpg', cv2.IMREAD_GRAYSCALE)
# img4 = cv2.imread('Aufgabe3/img/dva4_half_res.jpg', cv2.IMREAD_GRAYSCALE)
# img5 = cv2.imread('Aufgabe3/img/dva5_half_res.jpg', cv2.IMREAD_GRAYSCALE)

title = 'depth map estimation'
cv2.namedWindow(title, cv2.WINDOW_GUI_NORMAL)

depth_maps = []
# Create depth maps from all possible combinations of the 3 images.
depth_maps.append(getDepthMap(img1, img2))
depth_maps.append(getDepthMap(img1, img3))
depth_maps.append(getDepthMap(img2, img3))

# Use img1 and create depth maps with the other 4 images.
# depth_maps.append(getDepthMap(img1, img2))
# depth_maps.append(getDepthMap(img1, img3))
# depth_maps.append(getDepthMap(img1, img4))
# depth_maps.append(getDepthMap(img1, img5))

# Combine depth maps to result.
depth_map = np.zeros(depth_maps[0].shape)

for i in range(len(depth_maps)):
    depth_map += depth_maps[i]

depth_map = depth_map / 3 / 255

# Show result.
cv2.imshow(title, depth_map)
cv2.imwrite('Aufgabe3/result.png', depth_map * 255)
cv2.waitKey(0)
