"""Internal module that keeps utils to be used by console scripts."""

from argparse import ArgumentTypeError


def check_positive_int_or_raise(value):
    """Check passed value is a positive integer.

    :return: value if it passes the check
    :raises ArgumentTypeError: if passed value not positive
    """

    try:
        if value != int(value):
            raise ArgumentTypeError('{} is not an integer'.format(value))
    except ValueError as value_error:
        raise ArgumentTypeError('{} is not an integer (detailed error: {})'
                                ''.format(value, value_error))

    if value <= 0:
        raise ArgumentTypeError('{} is not a positive integer'.format(value))

    return value


def check_non_existing_file_or_raise(path):
    """Check passed path is a non-existing file path.

    :return: path if it passes the check
    :raises ArgumentTypeError: if passed value already exists
    """

    pass
