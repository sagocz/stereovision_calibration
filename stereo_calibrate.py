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
    objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)

    objp = objp * square_size  # Create real world coords. Use your metric.

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    first_imgpoints = []  # 2d points in image plane.
    second_imgpoints = []  # 2d points in image plane.

    # First directory path correction. Remove the last character if it is '/'
    if first_dir[-1:] == '/':
        first_dir = first_dir[:-1]

    # Second directory path correction. Remove the last character if it is '/'
    if second_dir[-1:] == '/':
        second_dir = second_dir[:-1]

    first_images = glob.glob(r'data\left_fixed_stereo\*.png')
    second_images = glob.glob(r'data\right_fixed_stereo\*.png')

    first_images.sort()
    second_images.sort()

        # Pairs should be same size. Otherwise we have sync problem.
    if len(first_images) != len(second_images):
        print("Liczba obrazow z pierwszej kamery, nie jest równa drugiej")
        print("First images count: ", len(first_images))
        print("Second images count: ", len(second_images))
        sys.exit(-1)

    pair_images = zip(first_images, second_images)  # Pair the images for single loop handling
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

    image_size = gray_second.shape  # If you have no acceptable pair, you may have an error here.
    return [objpoints, first_imgpoints, second_imgpoints]

def stereoCalibrate(first_file, second_file, first_dir, second_dir, first_prefix, second_prefix, square_size, save_file):

    objp, firstp, secondp = loadImagePoints(first_dir, first_prefix, second_dir, second_prefix, square_size)

    K1, D1 = loadCoefficients(first_file)
    K2, D2 = loadCoefficients(second_file)

    flag = 0

    flag |= cv2.CALIB_USE_INTRINSIC_GUESS

    ret, K1, D1, K2, D2, R, T, E, F = cv2.stereoCalibrate(objp, firstp, secondp, K1, D1, K2, D2, image_size)
    print("Stereo calibration rms:", ret)
    R1, R2, P1, P2, Q, roi_first, roi_second = cv2.stereoRectify(K1, D1, K2, D2, image_size, R, T, flags = cv2.CALIB_ZERO_DISPARITY, alpha = 0.9)

    saveStereoCoefficients(save_file, K1, D1, K2, D2, R, T, E, F, R1, R2, P1, P2, Q)

if __name__ == '__main__':

    # first_file & second_file string with example_single_cam_params.yaml
    # first_dir & second_dir string with images_fixed_stereo - folder with fixed
    # first_prefix & second_prefix with first / second etc < this is the img file description
    # square_size < that a float type variable for scalling points into real world coordinates
    # save_file < the name of file with stereo params

    parser = argparse.ArgumentParser(description='Camera calibration')

    parser.add_argument('--first_file', type=str, required=True, help='first matrix file')
    parser.add_argument('--second_file', type=str, required=True, help='second matrix file')
    parser.add_argument('--first_dir', type=str, required=True, help='first images directory path')
    parser.add_argument('--second_dir', type=str, required=True, help='second images directory path')
    parser.add_argument('--first_prefix', type=str, required=True, help='first image prefix')
    parser.add_argument('--second_prefix', type=str, required=True, help='second image prefix')
    parser.add_argument('--square_size', type=float, required=False, help='chessboard square size')
    parser.add_argument('--save_file', type=str, required=True, help='YML file to save stereo calibration matrices')

    args = parser.parse_args()

    stereoCalibrate(args.first_file, args.second_file, args.first_dir, args.second_dir, args.first_prefix, args.second_prefix, args.square_size, args.save_file)