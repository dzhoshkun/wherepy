"""Internal module that keeps the abstract Tracker class."""


class Tracker(object):
    """This class is an abstraction for all supported trackers."""

    NOT_IMPLEMENTED_MSG = 'To be implemented in device-linked class'

    def __init__(self):
        """Create an instance ready for connecting."""
        self.__connected = False

    def connect(self):
        """Connect to tracking device.

        :raise IOError: if no tracking device found
        """
        raise NotImplementedError(Tracker.NOT_IMPLEMENTED_MSG)

    def disconnect(self):
        """Disconnect from tracking device.

        :raise IOError: if not connected
        """
        raise NotImplementedError(Tracker.NOT_IMPLEMENTED_MSG)

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

        # pylint:disable=unused-argument

        raise NotImplementedError(Tracker.NOT_IMPLEMENTED_MSG)
