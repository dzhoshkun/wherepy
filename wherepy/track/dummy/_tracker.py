"""Internal module that keeps the Tracker class for generating random data."""

from random import (random, uniform)
from math import sqrt
import wherepy.track


class Tracker(wherepy.track.Tracker):
    """This class generates random tracking data."""

    def __init__(self):
        """Create an instance ready for connecting."""
        super(Tracker, self).__init__()

    def connect(self):
        if self.connected:
            return

        self.__connected = True

    def disconnect(self):
        if not self.connected:
            raise IOError('Not connected')

        self.__connected = False

    def capture(self, tool_id):
        if not self.connected:
            raise IOError('Not connected')

        # generate a random quaternion
        quaternion = [uniform(0.0, 1000.0) for _ in range(4)]
        norm = reduce(lambda value_1, value_2: value_1 + value_2,
                      map(lambda value: pow(value, 2), quaternion))
        norm = sqrt(norm)
        quaternion = list(map(lambda value: value / norm, quaternion))

        # generate a random transform in a hypothetical
        # tracking volume of 1 m3
        coordinates = [uniform(-500.0, 500.0) for _ in range(3)]

        # an artificial measure of quality based on a
        # maximum allowable error of 0.8 mm
        quality_min, quality_max = 0.00, 1.00  # %
        error_min, error_max = 0.00, 0.80  # mm
        error_range = error_max - error_min

        # generate a random error value
        error = random()

        if error > error_max:
            quality = quality_min
        else:
            quality = quality_max * (error_max - error)
            quality += quality_min * (error - error_min)
            quality /= error_range

        # return a tool pose with the generated values
        return wherepy.track.ToolPose(
            tid=tool_id, quaternion=quaternion, coordinates=coordinates,
            quality=quality, error=error,
        )
