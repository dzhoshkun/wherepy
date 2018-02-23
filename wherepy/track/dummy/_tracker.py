"""Internal module that keeps the Tracker class for generating random data."""

from random import (random, uniform, randrange)
from math import sqrt
import wherepy.track


class Tracker(wherepy.track.Tracker):
    """This class generates random tracking data."""

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

        # should I stay or should I go? :)
        moody_perc = 20
        if randrange(0, 100) < moody_perc:
            raise IOError('I am moody {} % of the time'.format(moody_perc))

        # generate a random quaternion
        quaternion = [uniform(0.0, 1000.0) for _ in range(4)]
        norm = reduce(lambda value_1, value_2: value_1 + value_2,
                      [pow(value, 2) for value in quaternion])
        norm = sqrt(norm)
        quaternion = [value / norm for value in quaternion]

        # generate a random transform in a hypothetical
        # tracking volume of 1 m3
        coordinates = [uniform(-500.0, 500.0) for _ in range(3)]

        # generate a random error value
        error = random()

        # compute the corresponding quality, based on an artificial
        # 0.8 mm maximum allowable error
        quality = wherepy.track.utils.quality(error, 0.8, 0.1)

        # return a tool pose with the generated values
        return wherepy.track.ToolPose(
            tid=tool_id, quaternion=quaternion, coordinates=coordinates,
            quality=quality, error=error,
        )
