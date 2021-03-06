"""Internal module that keeps utils to be used by console scripts."""

from argparse import ArgumentTypeError
from os.path import exists


def check_positive_int(value):
    """Check passed value is a positive integer.

    :return: value if it passes the check
    :raises ArgumentTypeError: if passed value not positive
    """

    try:
        _value = int(value)
        if _value != float(value):
            raise ArgumentTypeError('{} is not an integer'.format(value))
    except ValueError as value_error:
        raise ArgumentTypeError('{} is not an integer (detailed error: {})'
                                ''.format(value, value_error))

    if _value <= 0:
        raise ArgumentTypeError('{} is not a positive integer'.format(value))

    return _value


def check_non_existing(path):
    """Check passed path is a non-existing file path.

    :return: path if it passes the check
    :raises ArgumentTypeError: if passed value already exists
    """

    if exists(path):
        raise ArgumentTypeError('{} already exists'.format(path))

    return path
