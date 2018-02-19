"""Internal module that keeps the Tracker class for NDI devices."""

import wherepy.track


class Tracker(wherepy.track.Tracker):
    """This class is an abstraction for NDI trackers."""

    def __init__(self):
        """Create an instance ready for connecting."""
        super(Tracker, self).__init__()

    def connect(self):
        super(Tracker, self).connect()

    def disconnect(self):
        super(Tracker, self).disconnect()

    def capture(self, tool_id):
        return super(Tracker, self).capture(tool_id)
