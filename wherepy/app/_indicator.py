"""Internal module that keeps the live tracking quality indicator
functionality.

"""

from time import sleep
from sys import stdout

WIDTHS = None


def display_status(connected, quality=None, error=None, msg=None, utf=False):
    """Display status of tracking data on the CLI.

    :param connected: whether a tracking device is connected
    :type connected: bool
    :param quality: tracking signal quality indicator
    :type quality: float between 0.00 and 1.00
    :param error: tracking error
    :type error: float (mm)
    :param msg: an optional info message
    :type msg: str
    :param utf: whether to use Unicode symbols
    """

    global WIDTHS
    if not WIDTHS:
        WIDTHS = [10, 19, 11, 26]
        header = '|{}'.format('Device'.center(WIDTHS[0]))
        header += '|{}'.format('Signal'.center(WIDTHS[1]))
        header += '|{}'.format('Error'.center(WIDTHS[2]))
        header += '|{}|'.format('Info'.center(WIDTHS[3]))
        stdout.write('{}\n'.format(header))

        separator = '-' * (sum(WIDTHS) + (1 + len(WIDTHS)))
        stdout.write('{}\n'.format(separator))

    status = ''

    if utf:
        import _symbols_unicode
        symbols = _symbols_unicode.INDICATOR_SYMBOLS
    else:
        import _symbols_ascii
        symbols = _symbols_ascii.INDICATOR_SYMBOLS
    if connected:
        connection_status = symbols['connection_status']['connected']
    else:
        connection_status = symbols['connection_status']['not connected']
    connection_status = '[{}]'.format(connection_status).center(WIDTHS[0] + 1)
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
    signal_status = '[{}] {:2d} %'.format(
        signal_status, int(100 * quality)).center(WIDTHS[1] + 1)
    status += '{}'.format(signal_status)

    error_status = 'NA'
    if error:
        if error == float('inf'):
            error_status = '  ~  '
        else:
            error_status = '{:.2f} mm'.format(error)
    error_status = '{}'.format(error_status.center(9)).center(WIDTHS[2] + 1)
    status += '{}'.format(error_status)

    if msg:
        status += '{}'.format(msg[:WIDTHS[3] - 1]).center(WIDTHS[3] + 1)
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
