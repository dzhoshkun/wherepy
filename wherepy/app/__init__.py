"""Functions that implement the functionality of console scripts."""

from argparse import ArgumentParser
from wherepy.track.ndi import Tracker
from wherepy.io import SessionLog
from ._utils import (check_positive_int_or_raise, check_non_existing_file_or_raise)
from ._indicator import run_indicator_cli
from ._collector import collect_n_poses_cli


def collector_cli():
    """Collect tracking data in CLI mode."""

    parser = ArgumentParser()
    parser.add_argument('-p', '--num-poses', help='Number of poses to capture',
                        type=check_positive_int_or_raise,
                        metavar='N', required=True)
    parser.add_argument('-o', '--session-log', help='Where to save captured poses',
                        type=check_non_existing_file_or_raise,
                        metavar='FILE', required=True)

    args = parser.parse_args()

    tracker = Tracker()
    session_log = SessionLog(args.session_log)
    collect_n_poses_cli(tracker=tracker, num_poses=args.num_poses, session_log=session_log)


def indicator_cli():
    """Live CLI tracking quality and error indicator."""

    tracker = Tracker()
    run_indicator_cli(tracker=tracker, update_rate=3)
