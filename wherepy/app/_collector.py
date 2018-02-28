"""This internal module keeps elements related to tracking data collection."""

from time import sleep
from wherepy.io import (display_header, display_status)

# pylint:disable=too-many-branches


def collect_n_poses_cli(tracker, num_poses, session_log, update_rate=10, utf=False):
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
    :param utf: whether to use Unicode symbols
    :return: ``True`` if collection of at least specified number of poses
    succeeds, ``False`` otherwise
    """

    update_interval = 1.0 / update_rate

    display_header()

    captured = 0
    for _ in range(3 * num_poses):
        quality, error = None, None
        if not tracker.connected:
            try:
                msg = 'Attempting to connect to device'
                display_status(tracker.connected, quality, error, msg, utf)

                tracker.connect()
            except IOError:
                msg = 'Could not connect to device'

        if tracker.connected:
            try:
                tool_pose = tracker.capture(tool_id=1)
            except IOError:
                msg = 'Out of tracking volume?'
            except ValueError:
                msg = 'Unsupported tool'
            else:
                session_log.append(tool_pose)
                captured += 1
                msg = 'Collected {} pose'.format(captured)
                if captured > 1:
                    msg += 's'
                quality, error = tool_pose.quality

        display_status(tracker.connected, quality, error, msg, utf)

        if captured >= num_poses:
            break

        sleep(update_interval)

    if tracker.connected:
        try:
            tracker.disconnect()
        except IOError:
            msg = 'Could not disconnect from device'

    if captured == 0:
        msg = 'Could not collect any poses'

    if captured < num_poses:
        msg = 'Collected only {} out of {} poses'.format(captured, num_poses)

    display_status(tracker.connected, quality, error, msg, utf)

    return captured >= num_poses
