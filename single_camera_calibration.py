import numpy as np
import cv2
import glob
import argparse
import time
from calibration_storage import saveCoefficients

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

width = 9
height = 6


def calibrate(dir_path, prefix, square_size):

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(8,6,0)
    objp = np.zeros((12*12,3), np.float32)
    objp[:,:2] = np.mgrid[0:12,0:12].T.reshape(-1,2)

    objp = objp * square_size

    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.
    
    if dir_path[-1:] == '/':
        dir_path = dir_path[:-1]

    #images = glob.glob(dir_path+'/' + prefix + '*.png')  
    images = glob.glob(r'data\right_png\*.png') 
    print("Rozpoczęto proces kalibracji ...")
    for fname in images:

        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('Kalibrowany obraz1', img)
        ret, corners = cv2.findChessboardCorners(gray, (12,12), None)
        
        if ret:
            
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

            img = cv2.drawChessboardCorners(img, (12, 12), corners2, ret)
            # cv2.imshow('Kalibrowany obraz', img)
            print("Pomyślnie skalibrowany obraz: " + str(len(objpoints)))
            
    
        else: print("Błędny obraz ...")

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    return [ret, mtx, dist, rvecs, tvecs]


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Camera calibration')

    parser.add_argument('--image_dir', type=str, required=False, help='image directory path')
    parser.add_argument('--prefix', type=str, required=True, help='image prefix')
    parser.add_argument('--square_size', type=float, required=False, help='chessboard square size')
    parser.add_argument('--save_file', type=str, required=True, help='YML file to save calibration matrices')
    args = parser.parse_args()

    ret, mtx, dist, rvecs, tvecs = calibrate(args.image_dir, args.prefix, args.square_size)
    # calibrate(args.image_dir, args.prefix, args.square_size)
    saveCoefficients(mtx, dist, args.save_file)

    print("End of calibration.")
    print("RMS = " + str(ret))