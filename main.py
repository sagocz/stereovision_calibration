import argparse

from src.calibration_manager import CalibrationManager


def main(*args, **kwargs):
    manager = CalibrationManager(args.config)
    manager.execute()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Single and Stereo camera calibration tool")
    parser.add_argument(
        "--config", type=str, required=True, help="Configuration yaml file"
    )
    args = parser.parse_args()
    main(args)
