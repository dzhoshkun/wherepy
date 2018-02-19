"""Internal module that keeps the live tracking quality indicator
functionality.

"""

from time import sleep


def compose_indicator(filled, bar, msg=None):
    if msg:
        status = msg
    else:
        num_bars = int(filled / 0.1)
        num_spaces = 10 - num_bars
        status = bar * num_bars
        status += ' ' * num_spaces
    return '|{}|'.format(status)


def run_indicator_cli(tracker, update_rate=10):
    """Run live CLI quality indicator of passed tracker at desired
    update rate.

    :param tracker: query this tracker
    :type tracker: Tracker
    :param update_rate: update rate in Hz
    :type update_rate: int
    """
    update_interval = 1.0 / update_rate
    try:
        tracker.connect()
    except IOError:
        pass
    while True:
        if not tracker.connected:
            quality = None
            error = None
            msg = 'NO CONNECTION'
        else:
            try:
                tool_pose = tracker.capture(tool_id=1)
            except IOError:
                quality = 0.0
                error = float('inf')
                msg = 'OUT-OF-VOLUME'
            except ValueError:
                quality = None
                error = None
                msg = 'UNSUPPORTED TOOL'
            else:
                quality, error = tool_pose.quality
                msg = None

        status = ''

        status += 'Signal:  '
        status += compose_indicator(quality, '>', msg)
        status += '  {:5d} %\n'.format(int(100 * quality))

        status += 'Error:   '
        status += compose_indicator(1 - quality, '<', msg)
        status += '  {:5.2f} mm\n'.format(error)

        print(status)
        sleep(update_interval)
