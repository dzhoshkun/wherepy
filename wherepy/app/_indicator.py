# -*- coding: utf-8 -*-

"""Internal module that keeps the live tracking quality indicator
functionality.

"""

from time import sleep
from sys import stdout


def display_status(connected, quality=None, error=None, msg=None):
    """Display status of tracking data in the following format:
    | Device [✓] | Signal [=====     ] 54 % | Error  1.54 mm  | info message here.       |
    | Device [✗] | Signal [          ]  0 % | Error     ~     |

    :param connected: whether a tracking device is connected
    :type connected: bool
    :param quality: tracking signal quality indicator
    :type quality: float between 0.00 and 1.00
    :param error: tracking error
    :type error: float (mm)
    :param msg: an optional info message
    :type msg: str
    """
    status = ''
    if connected:
        connection_status = '✓'  # u'\u2713'
    else:
        connection_status = '✗'  # u'\u2717'
    connection_status = 'Device [{}]'.format(connection_status).center(14)
    status += '|{}'.format(connection_status)

    total_bars = 10
    quality_bars = 0
    space_bars = total_bars - quality_bars
    arrow = ''
    if quality:
        quality_bars = int(quality / (1.0 / total_bars))
        space_bars = total_bars - quality_bars
        if quality_bars - 1 > 0:
            quality_bars -= 1
            arrow = '>'
    signal_status = '=' * quality_bars
    signal_status += arrow
    signal_status += ' ' * space_bars
    signal_status = 'Signal [{}] {:2d} %'.format(signal_status, int(100 * quality)).center(26)
    status += '|{}'.format(signal_status)

    error_status = 'NA'
    if error:
        if error == float('inf'):
            error_status = '  ~  '
        else:
            error_status = '{:.2f} mm'.format(error)
    error_status = 'Error {}'.format(error_status.center(9)).center(17)
    status += '|{}|'.format(error_status)

    if msg:
        status += ' {} |'.format(msg[:24]).ljust(24)
    else:
        status += ' ' * 27

    stdout.write('{}\r'.format(status))
    stdout.flush()


def run_indicator_cli(tracker, update_rate=10):
    """Run live CLI quality indicator of passed tracker at desired
    update rate.

    :param tracker: query this tracker
    :type tracker: Tracker
    :param update_rate: update rate in Hz
    :type update_rate: int
    """
    update_interval = 1.0 / update_rate

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

        display_status(tracker.connected, quality, error, msg)
        sleep(update_interval)
