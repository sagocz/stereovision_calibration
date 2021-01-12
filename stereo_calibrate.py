import numpy as np
import cv2
import glob
import argparse
import sys
from calibration_storage import loadCoefficients, saveStereoCoefficients

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
image_size = None

def loadImagePoints(first_dir, first_prefix, second_dir, second_prefix, square_size):

    global image_size

    pattern_size = (9,6)

    objp = np.zeros((9 * 6, 3), np.float32)
    objp[:, :2] = np.mgrid[0:width, 0:height].T.reshape(-1, 2)

    objp = objp * square_size  # Create real world coords. Use your metric.

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    first_imgpoints = []  # 2d points in image plane.
    second_imgpoints = []  # 2d points in image plane.

    # First directory path correction. Remove the last character if it is '/'
    if first_dir[-1:] == '/':
        left_dir = left_dir[:-1]

    # Second directory path correction. Remove the last character if it is '/'
    if second_dir[-1:] == '/':
        right_dir = right_dir[:-1]

    first_images = glob.glob(first_dir + '/' + first_prefix + '*.png')
    second_images = glob.glob(second_dir + '/' + second_prefix + '*.png')

    first_images.sort()
    second_images.sort()

        for first_im, second_im in pair_images:
        # Right Object Points
        second = cv2.imread(second_im)
        gray_second = cv2.cvtColor(second, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret_second, corners_second = cv2.findChessboardCorners(gray_second, pattern_size, cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_FILTER_QUADS)

        # Left Object Points
        first = cv2.imread(first_im)
        gray_first = cv2.cvtColor(first, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret_first, corners_first = cv2.findChessboardCorners(gray_first, pattern_size, cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_FILTER_QUADS)

            if ret_first and ret_second:  # If both image is okay. Otherwise we explain which pair has a problem and continue
            # Object points
            objpoints.append(objp)
            # Right points
            corners2_second = cv2.cornerSubPix(gray_second, corners_second, (5, 5), (-1, -1), criteria)
            second_imgpoints.append(corners2_second)
            # Left points
            corners2_first = cv2.cornerSubPix(gray_first, corners_first, (5, 5), (-1, -1), criteria)
            first_imgpoints.append(corners2_first)
        else:
            print("Chessboard couldn't detected. Image pair: ", first_im, " and ", second_im)
            continue

    image_size = gray_right.shape  # If you have no acceptable pair, you may have an error here.
    return [objpoints, left_imgpoints, right_imgpoints]
def stereoCalibrate(first_file, second_file, first_dir, second_dir, first_prefix, second_prefix, square_size)

    objp, leftp, rightp = load_image_points()