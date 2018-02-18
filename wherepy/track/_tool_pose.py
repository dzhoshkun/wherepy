"""Internal module that keeps the ToolPose class."""

from time import time


class ToolPose(object):
    """Abstraction for timestamped tracking data of a tool."""

    def __init__(self, tid, quaternion, coordinates, quality, error, timestamp=time()):
        """Construct a new tool pose with given data.

        :param tid: a device-specific ID value for unambiguously resolving tools
        :type tid: should not be ``None``
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

        # pylint:disable=too-many-arguments

        self.__id = tid
        self.__quaternion = quaternion
        self.__coordinates = coordinates
        self.__quality = quality
        self.__error = error
        self.__timestamp = timestamp

    @property
    def tid(self):
        """Get this tool's ID."""
        return self.__tid

    @tid.setter
    def tid(self, tid):
        """Do nothing: setting deliberately disallowed."""
        pass

    @property
    def quaternion(self):
        """Get this tool's quaternion."""
        return self.__quaternion

    @quaternion.setter
    def quaternion(self, quaternion):
        """Do nothing: setting deliberately disallowed."""
        pass

    @property
    def coordinates(self):
        """Get this tool's coordinates."""
        return self.__coordinates

    @coordinates.setter
    def coordinates(self, coordinates):
        """Do nothing: setting deliberately disallowed."""
        pass

    @property
    def quality(self):
        """Get this pose's tracking quality, and error values.

        :return: ``quality, error``
        """
        return self.__quality, self.__error

    @quality.setter
    def quality(self, quality):
        """Do nothing: setting deliberately disallowed."""
        pass

    @property
    def timestamp(self):
        """Get this pose's capture timestamp."""
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Do nothing: setting deliberately disallowed."""
        pass
