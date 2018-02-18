import unittest
from wherepy.track import ToolPose


class ToolPoseTestCase(unittest.TestCase):

    def test_id_validity_checked(self):
        self.__fail()

    def test_quaternion_validity_checked(self):
        self.__fail()

    def test_coordinates_validity_checked(self):
        self.__fail()

    def test_quality_validity_checked(self):
        self.__fail()

    def test_timestamp_validity_checked(self):
        self.__fail()

    def __fail(self):
        self.fail('not implemented')
