"""Internal module that keeps the live tracking quality indicator
functionality.

"""

# pylint:disable=too-many-locals

from time import sleep
from sys import stdout


def get_field_widths():
    """Get a list of the width of all status fields."""

    return [10, 19, 11, 26]


def display_header():
    """Display tracking data status header on the CLI."""

    widths = get_field_widths()

    header = '|{}'.format('Device'.center(widths[0]))
    header += '|{}'.format('Signal'.center(widths[1]))
    header += '|{}'.format('Error'.center(widths[2]))
    header += '|{}|'.format('Info'.center(widths[3]))
    stdout.write('{}\n'.format(header))

    separator = '-' * (sum(widths) + (1 + len(widths)))
    stdout.write('{}\n'.format(separator))


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

    widths = get_field_widths()
    status = ''

    # pylint:disable=relative-import
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
    connection_status = '[{}]'.format(connection_status).center(widths[0] + 1)
    if utf:
        status += '  '
    status += '{}'.format(connection_status)

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
        signal_status, int(100 * quality)).center(widths[1] + 1)
    status += ' {}'.format(signal_status)

    error_status = 'NA'
    if error:
        if error == float('inf'):
            error_status = '  ~  '
        else:
            error_status = '{:.2f} mm'.format(error)
    error_status = '{}'.format(error_status.center(9)).center(widths[2] + 1)
    status += ' {}'.format(error_status)

    if msg:
        status += ' {}'.format(msg[:widths[3] - 1]).center(widths[3] + 1)
    else:
        status += ' ' * 27

    stdout.write('{}\r'.format(status))
    stdout.flush()


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
