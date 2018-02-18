"""Internal module that keeps the ToolPose class."""

from time import time


class ToolPose(object):
    """Abstraction for timestamped tracking data of a tool."""

    def __init__(self, id, quaternion, coordinates, quality, error, timestamp=time()):
        """Construct a new tool pose with given data.

        :param id: a device-specific ID value for unambiguously resolving tools
        :type id: should not be ``None``
        :param quaternion: together with coordinates, this makes the actual pose
        :type quaternion: quadruple, or anything that has four numeric values
        :param coordinates: together with quaternion, this makes the actual pose
        :type coordinates: triple, or anything that has four numeric values
        :param quality: quality of tracking data, with quality directly proportional
        to value
        :type quality: float between 0.00 and 1.00 (representing a percentage)
        :param error: This is a device-specific record of tracking error for this pose
        :type error: anything, even ``None``
        :param timestamp: when this tool pose was captured
        :type timestamp: a valid value in seconds as per
        https://docs.python.org/2/library/time.html#time.time
        :raise ValueError: if any of the given parameters are invalid
        """
        self.__id = id
        self.__quaternion = quaternion
        self.__coordinates = coordinates
        self.__quality = quality
        self.__error = error
        self.__timestamp = timestamp
