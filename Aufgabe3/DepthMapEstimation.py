# Code adapted from
# https://docs.opencv2.org/4.5.5/da/de9/tutorial_py_epipolar_geometry.html
# and https://www.andreasjakl.com/understand-and-apply-stereo-rectification-
# for-depth-maps-part-2/
import cv2
from cv2 import waitKey
import numpy as np

# load left and right images
img1 = cv2.imread('Aufgabe3/tsukuba01.jpg', 0)
img2 = cv2.imread('Aufgabe3/tsukuba02.jpg', 0)
img3 = cv2.imread('Aufgabe3/tsukuba03.jpg', 0)
title = 'window'
cv2.namedWindow(title, cv2.WINDOW_GUI_NORMAL)


# Draw epilines
def drawLines(img1, img2, lines, pts1, pts2):
    r, c = img1.shape
    img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
    img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
    for r, pt1, pt2 in zip(lines, pts1, pts2):
        color = tuple(np.random.randint(0, 255, 3).tolist())
        x0, y0 = map(int, [0, -r[2]/r[1]])
        x1, y1 = map(int, [c, -(r[2]+r[0]*c)/r[1]])
        img1 = cv2.line(img1, (x0, y0), (x1, y1), color, 1)
        img1 = cv2.circle(img1, tuple(pt1), 5, color, -1)
        img2 = cv2.circle(img2, tuple(pt2), 5, color, -1)
    return img1, img2


def estimateDepthMap(_img1, _img2):
    # find the keypoints and descriptors using SIFT_create
    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(_img1, None)
    kp2, des2 = sift.detectAndCompute(_img2, None)
    print('Found %d keypoints in the left image.' % len(kp1))
    print('Found %d keypoints in the right image.' % len(kp2))
    print('Each SIFT keypoint is described with a %s-d array' % des1.shape[1])

    # Visualize the SIFT keypoints
    imgSift1 = cv2.drawKeypoints(
        _img1, kp1, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    imgSift2 = cv2.drawKeypoints(
        _img2, kp2, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    cv2.imshow(title, np.concatenate((imgSift1, imgSift2), axis=1))
    cv2.waitKey(0)

    # match the keypoints using a FlannBasedMatcher
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    matchesMask = [[0, 0] for i in range(len(matches))]
    pts1 = []
    pts2 = []

    # ratio test as per Lowe's paper
    # only use matches with a reasonable small distance
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.8*n.distance:
            matchesMask[i] = [1, 0]
            pts2.append(kp2[m.trainIdx].pt)
            pts1.append(kp1[m.queryIdx].pt)

    # Now we have the list of best matches from both the images.
    # Let's find the Fundamental Matrix.
    pts1 = np.int32(pts1)
    pts2 = np.int32(pts2)
    assert(len(pts1) == len(pts2))
    print('Found %d matching keypoints in both images.' % len(pts1))

    # Now we compute the fundamental matrix
    F, mask = cv2.findFundamentalMat(pts1, pts2, cv2.FM_RANSAC)
    print('\nFundamental matrix\n', '\n'.join(['\t'.join(
        ['%03.4f' % cell for cell in row]) for row in F]))

    # Visualize the epilines
    # We select only inlier points
    pts1 = pts1[mask.ravel() == 1]
    pts2 = pts2[mask.ravel() == 1]

    # Find epilines corresponding to points in right image (second image) and
    # drawing its lines on left image
    lines1 = cv2.computeCorrespondEpilines(pts2.reshape(-1, 1, 2), 2, F)
    lines1 = lines1.reshape(-1, 3)
    img5, img6 = drawLines(_img1, _img2, lines1, pts1, pts2)

    # Find epilines corresponding to points in left image (first image) and
    # drawing its lines on right image
    lines2 = cv2.computeCorrespondEpilines(pts1.reshape(-1, 1, 2), 1, F)
    lines2 = lines2.reshape(-1, 3)
    img3, img4 = drawLines(_img2, _img1, lines2, pts2, pts1)
    cv2.imshow(title, np.concatenate((img3, img5), axis=1))
    cv2.waitKey(0)

    # https://www.andreasjakl.com/understand-and-apply-stereo-rectification-for-depth-maps-part-2/
    h1, w1 = img1.shape
    h2, w2 = img2.shape
    _, H1, H2 = cv2.stereoRectifyUncalibrated(
        np.float32(pts1),
        np.float32(pts2),
        F,
        imgSize=(w1, h1)
    )

    img1_rectified = cv2.warpPerspective(_img1, H1, (w1, h1))
    img2_rectified = cv2.warpPerspective(_img2, H2, (w2, h2))
    cv2.imshow(title, np.concatenate((img1_rectified, img2_rectified), axis=1))
    cv2.waitKey(0)

    # Matched block size. It must be an odd number >=1 .
    # Normally, it should be somewhere in the 3..11 range.
    block_size = 3
    min_disp = -16
    max_disp = 32
    # Maximum disparity minus minimum disparity.
    # The value is always greater than zero.
    # In the current implementation, this parameter must be divisible by 16.
    num_disp = max_disp - min_disp
    # Margin in percentage by which the best (minimum) computed cost function
    # value should "win" the second best value to consider
    # the found match correct.
    # Normally, a value within the 5-15 range is good enough
    uniquenessRatio = 5
    # Maximum size of smooth disparity regions to consider their noise
    # speckles and invalidate.
    # Set it to 0 to disable speckle filtering.
    # Otherwise, set it somewhere in the 50-200 range.
    speckleWindowSize = 100
    # Maximum disparity variation within each connected component.
    # If you do speckle filtering, set the parameter to a positive value,
    # it will be implicitly multiplied by 16.
    # Normally, 1 or 2 is good enough.
    speckleRange = 2
    disp12MaxDiff = 0

    stereo = cv2.StereoSGBM_create(
        minDisparity=min_disp,
        numDisparities=num_disp,
        blockSize=block_size,
        uniquenessRatio=uniquenessRatio,
        speckleWindowSize=speckleWindowSize,
        speckleRange=speckleRange,
        disp12MaxDiff=disp12MaxDiff,
        P1=8 * 1 * block_size * block_size,
        P2=32 * 1 * block_size * block_size,
    )
    disparity_SGBM = stereo.compute(img1_rectified, img2_rectified)

    # Normalize the values to a range from 0..255 for a grayscale image
    disparity_SGBM = cv2.normalize(
        disparity_SGBM,
        disparity_SGBM,
        alpha=255,
        beta=0,
        norm_type=cv2.NORM_MINMAX
    )

    disparity_SGBM = np.uint8(disparity_SGBM)
    cv2.imshow(title, disparity_SGBM)
    waitKey(0)
    return disparity_SGBM


depth_map1 = estimateDepthMap(img1, img2)
depth_map2 = estimateDepthMap(img1, img3)
depth_map3 = estimateDepthMap(img2, img3)

# TODO combine depth maps to result

cv2.imshow("result", depth_map1)
cv2.waitKey(0)
