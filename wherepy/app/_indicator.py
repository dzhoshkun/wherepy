"""Internal module that keeps the live tracking quality indicator
functionality.

"""

from time import sleep
from wherepy.io import (display_header, display_status)


def run_indicator_cli(tracker, update_rate=10, utf=False):
    """Run live CLI quality indicator of passed tracker at desired
    update rate.

    :param tracker: query this tracker
    :type tracker: Tracker
    :param update_rate: update rate in Hz
    :type update_rate: int
    :param utf: whether to use Unicode symbols
    """
    update_interval = 1.0 / update_rate

    display_header()

    while True:
        quality = None
        error = None
        msg = None

        if not tracker.connected:
            try:
                tracker.connect()
            except IOError:
                pass

        if tracker.connected:
            try:
                tool_pose = tracker.capture(tool_id=1)
            except IOError:
                quality = 0.0
                error = float('inf')
                msg = 'Out of tracking volume?'
            except ValueError:
                msg = 'Unsupported tool'
            else:
                quality, error = tool_pose.quality

        display_status(tracker.connected, quality, error, msg, utf)
        sleep(update_interval)
