"""Internal module that keeps the SessionLog class."""


class SessionLog(object):
    """This class takes care of logging all tracking data."""

    def __init__(self, filepath):
        """Create a blank session file in passed path.

        :param filepath: taken as-is, with absolutely no
        manipulation
        :raise OSError: if file creation fails for any reason
        """
        pass

    def append(self, tool_pose):
        """Append passed tool pose to session file.

        :type tool_pose: ToolPose
        """
        pass
