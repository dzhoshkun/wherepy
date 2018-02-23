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
    min_quality, max_quality = 0.00, 1.00  # %

    if error > max_error:
        return min_quality

    if error < min_error:
        return max_quality

    return (max_quality * (max_error - error) +
            min_quality * (error - min_error)) /\
           (max_error - min_error)
