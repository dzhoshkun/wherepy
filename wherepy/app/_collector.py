"""This internal module keeps elements related to tracking data collection."""


def collect_n_poses_cli(tracker, num_poses, session_log, update_rate=10):
    """Start passed tracker, collect specified number of poses, and stop it.

    :param tracker: no sanity checks are performed on this passed object, it
    should be ready to start
    :type tracker: Tracker
    :param num_poses: number of poses to collect
    :type num_poses: int - must be positive, obviously, no sanity checks
    performed
    :param session_log: session log for saving captured poses
    :type session_log: SessionLog
    :param update_rate: update rate in Hz
    :type update_rate: int
    """

    pass
