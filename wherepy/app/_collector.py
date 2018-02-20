"""This internal module keeps elements related to tracking data collection."""

from time import sleep
import logging


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
    :return: ``True`` if collection of at least specified number of poses
    succeeds, ``False`` otherwise
    """

    update_interval = 1.0 / update_rate

    captured = 0
    for _ in range(3 * num_poses):
        if not tracker.connected:
            try:
                logging.info('Attempting to connect to device')
                tracker.connect()
            except IOError as io_error:
                logging.error('Could not connect to device. The'
                              ' error was {}'.format(io_error))

        if tracker.connected:
            try:
                tool_pose = tracker.capture(tool_id=1)
            except IOError as io_error:
                logging.error('Could not obtain tool pose. The'
                              ' error was {}'.format(io_error))
            except ValueError as value_error:
                logging.error('Could not obtain tool pose. The'
                              ' error was {}'.format(value_error))
            else:
                session_log.append(tool_pose)
                captured += 1

        if captured >= num_poses:
            break

        sleep(update_interval)

    if tracker.connected:
        try:
            tracker.disconnect()
        except IOError as io_error:
            logging.error('Could not disconnect from device. The'
                          ' error was {}'.format(io_error))

    if captured == 0:
        logging.error('Could not collect any poses')
        return False

    if captured < num_poses:
        logging.error('Could collect only {} poses'.format(captured))
        return False

    return True
