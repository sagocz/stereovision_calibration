# Camera Calibration Tool

## Description
A tool for camera calibration, supporting both single cameras (`SingleCameraCalibrator`) and stereo vision systems (`StereoCalibrator`). Configuration is done via YAML files, and the entire process is managed by `CalibrationManager`.

## Requirements
- Python 3.6+
- OpenCV (`cv2`)
- NumPy
- PyYAML

You can install the required dependencies using:
```bash
pip install -r requirements.txt
```

## Code Structure
- `SingleCameraCalibrator` - Class for calibrating a single camera.
- `StereoCalibrator` - Class for calibrating a stereo vision system.
- `CalibrationManager` - Manager that selects the appropriate calibration type based on the configuration file.
- `main.py` - Script to start the calibration process.

## Usage
### 1. Single Camera Calibration
Prepare a `config_single.yaml` file:
```yaml
type: "single"
image_dir: "data/right_png"
prefix: ""
square_size: 0.025
pattern_size: [12, 12]
save_file: "calibration_single.yml"
```
Run the calibration:
```bash
python main.py --config config_single.yaml
```

### 2. Stereo Calibration
Prepare a `config_stereo.yaml` file:
```yaml
type: "stereo"
square_size: 0.025
first_file: "stereo_left.png"
second_file: "stereo_right.png"
first_dir: "data/left_png"
second_dir: "data/right_png"
save_file: "calibration_stereo.yml"
```
Run the calibration:
```bash
python main.py --config config_stereo.yaml
```

## Results
After the calibration process is completed, the `calibration_single.yml` or `calibration_stereo.yml` file will contain the camera coefficients.

## Author
A tool designed for camera calibration in machine vision systems.

