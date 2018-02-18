"""Internal module that keeps the abstract Tracker class."""


class Tracker(object):
    """This class is an abstraction for all supported trackers."""

    def __init__(self):
        """Create an instance ready for connecting."""
        self.__connected = False

    def connect(self):
        """Connect to tracking device.

        :raise IOError: if no tracking device found
        """
        self.__raise_not_implemented()

    def disconnect(self):
        """Disconnect from tracking device.

        :raise IOError: if not connected
        """
        self.__raise_not_implemented()

    @property
    def connected(self):
        """Get connection status.

        :return: ``True`` if connected, ``False`` otherwise
        :rtype: bool
        """
        return self.__connected

    @connected.setter
    def connected(self, connected):
        """Do nothing: setting deliberately disallowed."""
        pass

    def capture(self, tool_id):
        """Capture a tool's pose.

        :rtype: ToolPose
        :raise IOError: if not connected
        :raise ValueError: if `tool_id` not valid
        """
        self.__raise_not_implemented()

    def __raise_not_implemented(self):
        """Internal method for unimplemented methods."""
        raise NotImplementedError('To be implemented in device-linked class')
