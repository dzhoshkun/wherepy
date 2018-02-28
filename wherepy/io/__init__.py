"""IO utilities."""

# pylint:disable=too-many-locals
# pylint:disable=too-many-branches

from sys import stdout
from ._session_log import SessionLog


def get_field_widths():
    """Get a list of the width of all status fields."""

    return [10, 20, 13, 41]


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

    status_fields = []

    # pylint:disable=relative-import
    if utf:
        from . import _symbols_unicode
        symbols = _symbols_unicode.INDICATOR_SYMBOLS
    else:
        from . import _symbols_ascii
        symbols = _symbols_ascii.INDICATOR_SYMBOLS
    connection_status = ' '
    if utf:
        connection_status += ' '
    connection_status += symbols['connection_status'][connected]
    status_fields.append(connection_status)

    if not quality:
        quality = 0.0
    total_bars = 10
    quality_bars = max(int(quality / (1.0 / total_bars)) - 1, 0)
    space_bars = total_bars - quality_bars - 1
    signal_status = '=' * quality_bars + '>' + ' ' * space_bars
    signal_status = '[{}] {:3d} %'.format(signal_status, int(100 * quality))
    status_fields.append(signal_status)

    error_status = ' '
    if error:
        if error <= float('inf'):
            error_status = '{:.2f} mm'.format(error)
    status_fields.append(error_status)

    if not msg:
        msg = ' '
    status_fields.append(msg)

    status = ' '.join(map(lambda label, width: label.center(width),
                          status_fields, get_field_widths()))
    status = ' {} '.format(status)
    stdout.write('{}\r'.format(status))
    stdout.flush()
