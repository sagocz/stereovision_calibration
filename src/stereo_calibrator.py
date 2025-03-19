import numpy as np
import cv2
import glob
import sys


class StereoCalibrator:
    def __init__(self, square_size):
        self.square_size = square_size
        self.image_size = None
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        self.pattern_size = (9, 6)
        self.objp = self._generate_object_points()

    def _generate_object_points(self):
        objp = np.zeros((self.pattern_size[0] * self.pattern_size[1], 3), np.float32)
        objp[:, :2] = np.mgrid[
            0 : self.pattern_size[0], 0 : self.pattern_size[1]
        ].T.reshape(-1, 2)
        return objp * self.square_size

    def _load_coefficients(self, path):
        cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)
        K = cv_file.getNode("K").mat()
        D = cv_file.getNode("D").mat()
        cv_file.release()
        return K, D

    def _save_stereo_coefficients(
        self, path, K1, D1, K2, D2, R, T, E, F, R1, R2, P1, P2, Q
    ):
        cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_WRITE)
        cv_file.write("K1", K1)
        cv_file.write("D1", D1)
        cv_file.write("K2", K2)
        cv_file.write("D2", D2)
        cv_file.write("R", R)
        cv_file.write("T", T)
        cv_file.write("E", E)
        cv_file.write("F", F)
        cv_file.write("R1", R1)
        cv_file.write("R2", R2)
        cv_file.write("P1", P1)
        cv_file.write("P2", P2)
        cv_file.write("Q", Q)
        cv_file.release()

    def load_image_points(self, first_dir, second_dir):
        objpoints, first_imgpoints, second_imgpoints = [], [], []
        first_images = sorted(glob.glob(f"{first_dir}/*.png"))
        second_images = sorted(glob.glob(f"{second_dir}/*.png"))

        if len(first_images) != len(second_images):
            print("Number of calibration images are not equal.")
            sys.exit(-1)

        for first_im, second_im in zip(first_images, second_images):
            first_gray = cv2.cvtColor(cv2.imread(first_im), cv2.COLOR_BGR2GRAY)
            second_gray = cv2.cvtColor(cv2.imread(second_im), cv2.COLOR_BGR2GRAY)

            ret_first, corners_first = cv2.findChessboardCorners(
                first_gray,
                self.pattern_size,
                cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_FILTER_QUADS,
            )
            ret_second, corners_second = cv2.findChessboardCorners(
                second_gray,
                self.pattern_size,
                cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_FILTER_QUADS,
            )

            if ret_first and ret_second:
                objpoints.append(self.objp)
                first_imgpoints.append(
                    cv2.cornerSubPix(
                        first_gray, corners_first, (5, 5), (-1, -1), self.criteria
                    )
                )
                second_imgpoints.append(
                    cv2.cornerSubPix(
                        second_gray, corners_second, (5, 5), (-1, -1), self.criteria
                    )
                )
            else:
                print(f"Chessboard not find in {first_im} and {second_im}")

        self.image_size = first_gray.shape[::-1]  # (width, height)
        return objpoints, first_imgpoints, second_imgpoints

    def calibrate(self, first_file, second_file, first_dir, second_dir, save_file):
        objpoints, first_imgpoints, second_imgpoints = self.load_image_points(
            first_dir, second_dir
        )
        K1, D1 = self._load_coefficients(first_file)
        K2, D2 = self._load_coefficients(second_file)

        ret, K1, D1, K2, D2, R, T, E, F = cv2.stereoCalibrate(
            objpoints,
            first_imgpoints,
            second_imgpoints,
            K1,
            D1,
            K2,
            D2,
            self.image_size,
        )
        print("Stereo calibration RMS error:", ret)

        R1, R2, P1, P2, Q, _, _ = cv2.stereoRectify(
            K1,
            D1,
            K2,
            D2,
            self.image_size,
            R,
            T,
            flags=cv2.CALIB_ZERO_DISPARITY,
            alpha=0.9,
        )
        self._save_stereo_coefficients(
            save_file, K1, D1, K2, D2, R, T, E, F, R1, R2, P1, P2, Q
        )
