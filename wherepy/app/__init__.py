"""Functions that implement the functionality of console scripts."""

from argparse import ArgumentParser
from wherepy.track.ndi import Tracker
from wherepy.io import SessionLog
from ._utils import (check_positive_int, check_non_existing)
from ._indicator import run_indicator_cli
from ._collector import collect_n_poses_cli


def collector_cli():
    """Collect tracking data in CLI mode."""

    parser = ArgumentParser()
    parser.add_argument('-p', '--num-poses', help='Number of poses to capture',
                        type=check_positive_int,
                        metavar='N', required=True)
    parser.add_argument('-o', '--session-log', help='Where to save captured poses',
                        type=check_non_existing,
                        metavar='FILE', required=True)

    args = parser.parse_args()

    tracker = Tracker()
    session_log = SessionLog(args.session_log)
    if not collect_n_poses_cli(tracker=tracker, num_poses=args.num_poses, session_log=session_log):
        exit(1)


def indicator_cli():
    """Live CLI tracking quality and error indicator."""

    parser = ArgumentParser()
    parser.add_argument('--pretty', help='Pretty formatting (uses Unicode characters)',
                        action='store_true')

    args = parser.parse_args()

    tracker = Tracker()
    run_indicator_cli(tracker=tracker, update_rate=3, utf=args.pretty)
