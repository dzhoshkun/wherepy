import unittest
from wherepy.track import ToolPose


class ToolPoseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # valid means not None
        cls.valid_tid = '1'
        cls.invalid_tid = None

        # validity means len() = 4 here
        # no other check is performed
        cls.valid_quaternion = [0.0, 1.0, 2.0, 3.0]
        cls.invalid_quaternion = [0.0, 1.0, 2.0]

        # validity means len() = 3 here
        # no other check is performed
        cls.valid_coordinates = [0.0, 1.0, 2.0]
        cls.invalid_coordinates = [0.0, 1.0, 2.0, 3.0]

        cls.valid_quality = 0.50
        cls.invalid_qualities = [-0.01, 1.01]

        cls.invalid_timestamp = -123456789.123456

    def test_id_validity_checked(self):
        with self.assertRaises(ValueError):
            ToolPose(tid=ToolPoseTestCase.invalid_tid,
                     quaternion=ToolPoseTestCase.valid_quaternion,
                     coordinates=ToolPoseTestCase.valid_coordinates,
                     quality=ToolPoseTestCase.valid_quality,
                     error=None
                     )

    def test_quaternion_validity_checked(self):
        with self.assertRaises(ValueError):
            ToolPose(tid=ToolPoseTestCase.valid_tid,
                     quaternion=ToolPoseTestCase.invalid_quaternion,
                     coordinates=ToolPoseTestCase.valid_coordinates,
                     quality=ToolPoseTestCase.valid_quality,
                     error=None
                     )

    def test_coordinates_validity_checked(self):
        with self.assertRaises(ValueError):
            ToolPose(tid=ToolPoseTestCase.valid_tid,
                     quaternion=ToolPoseTestCase.valid_quaternion,
                     coordinates=ToolPoseTestCase.invalid_coordinates,
                     quality=ToolPoseTestCase.valid_quality,
                     error=None
                     )

    def test_quality_validity_checked(self):
        for invalid_quality in ToolPoseTestCase.invalid_qualities:
            with self.assertRaises(ValueError):
                ToolPose(tid=ToolPoseTestCase.valid_tid,
                         quaternion=ToolPoseTestCase.valid_quaternion,
                         coordinates=ToolPoseTestCase.valid_coordinates,
                         quality=invalid_quality,
                         error=None
                         )

    def test_timestamp_validity_checked(self):
        with self.assertRaises(ValueError):
            ToolPose(tid=ToolPoseTestCase.valid_tid,
                     quaternion=ToolPoseTestCase.valid_quaternion,
                     coordinates=ToolPoseTestCase.valid_coordinates,
                     quality=ToolPoseTestCase.valid_quality,
                     error=None,
                     timestamp=ToolPoseTestCase.invalid_timestamp
                     )
