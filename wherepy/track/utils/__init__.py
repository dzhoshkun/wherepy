"""Utility functions for tracking data processing."""


def quality(error, max_error, min_error=0.0):
    """Compute a quality percentage, based on error.

    :param error:
    :param max_error: maximum allowable error
    :param min_error: all smaller values than this yield
    100 % quality
    :return: a value btw. 0.00 and 1.00, representing a
    percentage
    """
    return 0.0
