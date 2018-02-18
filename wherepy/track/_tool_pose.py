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

        if tid is None:
            raise ValueError('Tool ID cannot be None')
        self.__tid = tid

        if len(quaternion) != 4:
            raise ValueError('A quaternion has 4 elements')
        self.__quaternion = quaternion

        if len(coordinates) != 3:
            raise ValueError('A point in space has 3 coordinates')
        self.__coordinates = coordinates

        if not 0.00 <= quality <= 1.00:
            raise ValueError('Quality value should be between 0.00 and'
                             ' 1.00 ({} passed)'.format(quality))
        self.__quality = quality
        self.__error = error

        if timestamp <= 0.0:
            raise ValueError('A timestamp is usually a positive floating-'
                             'point value ({} passed)'.format(timestamp))
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
