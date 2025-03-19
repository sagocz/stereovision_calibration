import yaml

from src.single_camera_calibration import SingleCameraCalibrator
from src.stereo_calibrator import StereoCalibrator

class CalibrationManager:
    def __init__(self, config_path):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

    def execute(self):
        if self.config["type"] == "single":
            calibrator = SingleCameraCalibrator(self.config["square_size"], tuple(self.config["pattern_size"]))
            calibrator.calibrate(self.config["image_dir"], self.config["prefix"], self.config["save_file"])
        elif self.config["type"] == "stereo":
            calibrator = StereoCalibrator(self.config["square_size"])
            calibrator.calibrate(
                self.config["first_file"], self.config["second_file"],
                self.config["first_dir"], self.config["second_dir"],
                self.config["save_file"]
            )
        else:
            print("Unknown calibration type in configuration file.")