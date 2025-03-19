import numpy as np
import cv2
import glob


class SingleCameraCalibrator:
    def __init__(self, square_size, pattern_size=(12, 12)):
        self.square_size = square_size
        self.pattern_size = pattern_size
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        self.objp = self._generate_object_points()

    def _generate_object_points(self):
        objp = np.zeros((self.pattern_size[0] * self.pattern_size[1], 3), np.float32)
        objp[:, :2] = np.mgrid[
            0 : self.pattern_size[0], 0 : self.pattern_size[1]
        ].T.reshape(-1, 2)
        return objp * self.square_size

    def calibrate(self, image_dir, prefix, save_file):
        objpoints, imgpoints = [], []
        images = glob.glob(f"{image_dir}/{prefix}*.png")
        print("Starting calibration...")

        for fname in images:
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, self.pattern_size, None)

            if ret:
                objpoints.append(self.objp)
                corners2 = cv2.cornerSubPix(
                    gray, corners, (11, 11), (-1, -1), self.criteria
                )
                imgpoints.append(corners2)
                print(f"Image {fname} calibrated.")
            else:
                print(f"Image {fname} calibration failed.")

        ret, mtx, dist, _, _ = cv2.calibrateCamera(
            objpoints, imgpoints, gray.shape[::-1], None, None
        )
        self._save_coefficients(save_file, mtx, dist)
        print("Calibration finished. RMS:", ret)

    def _save_coefficients(self, path, K, D):
        cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_WRITE)
        cv_file.write("K", K)
        cv_file.write("D", D)
        cv_file.release()
