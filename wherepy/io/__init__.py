"""IO utilities."""

# pylint:disable=too-many-locals
# pylint:disable=too-many-branches

from sys import stdout
from ._session_log import SessionLog


def get_field_widths():
    """Get a list of the width of all status fields."""

    return [10, 19, 11, 36]


def get_field_labels():
    """Get a list of the field labels."""

    return ['Device', 'Signal', 'Error', 'Info']


def display_header():
    """Display tracking data status header on the CLI."""

    widths = get_field_widths()
    header = '|'.join(map(lambda label, width: label.center(width),
                          get_field_labels(), widths))
    header = '|{}|'.format(header)
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
        from . import _symbols_unicode
        symbols = _symbols_unicode.INDICATOR_SYMBOLS
    else:
        from . import _symbols_ascii
        symbols = _symbols_ascii.INDICATOR_SYMBOLS
    if connected:
        connection_status = symbols['connection_status']['connected']
    else:
        connection_status = symbols['connection_status']['not connected']
    connection_status = '{}'.format(connection_status).center(widths[0] + 1)
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
    else:
        quality = 0.0
    signal_status = '=' * quality_bars
    signal_status += arrow
    signal_status += ' ' * space_bars
    signal_status = '[{}] {:2d} %'.format(
        signal_status, int(100 * quality)).center(widths[1] + 1)
    status += ' {}'.format(signal_status)

    error_status = 'NA '
    if error:
        if error == float('inf'):
            error_status = '  ~  '
        else:
            error_status = '{:.2f} mm'.format(error)
    error_status = '{}'.format(error_status.center(9)).center(widths[2] + 1)
    status += ' {}'.format(error_status)

    if msg:
        status += ' {}'.format(msg[:widths[3] - 2]).center(widths[3])
    else:
        status += ' ' * (widths[3] + 1)

    stdout.write('{}\r'.format(status))
    stdout.flush()
