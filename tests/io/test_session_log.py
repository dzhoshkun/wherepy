import unittest
from os.path import (join, isfile)
from uuid import uuid4
from random import random
from yaml import load
from wherepy.io import SessionLog
from wherepy.track import ToolPose


class SessionLogTestCase(unittest.TestCase):

    @staticmethod
    def unique_string(length=6):
        return uuid4().hex[:length].upper()

    def setUp(self):
        self.tool_poses = []
        for i in range(10):
            self.tool_poses.append(
                ToolPose(tid='tool-{}'.format(i),
                         quaternion=[(i + 0.5) * j for j in range(4)],
                         coordinates=[(i + 1.5) * j for j in range(3)],
                         quality=random(),
                         error='error: {:010.0f}'.format(i + 2.5)
                         )
            )

    def test_invalid_filepath_raises(self):
        invalid_filepath = join('/', 'this', 'should-not', 'be-created', 'session.yml')
        with self.assertRaises(OSError):
            SessionLog(filepath=invalid_filepath)

    def test_existing_file_not_overwritten(self):
        filepath = 'session-{}.yml'.format(SessionLogTestCase.unique_string())
        SessionLog(filepath=filepath)
        with self.assertRaises(ValueError):
            SessionLog(filepath=filepath)

    def test_session_file_created(self):
        filepath = 'session-{}.yml'.format(SessionLogTestCase.unique_string())
        SessionLog(filepath=filepath)
        self.assertTrue(isfile(filepath))

    def test_tool_pose_appended_to_session_file(self):
        filepath = 'session-{}.yml'.format(SessionLogTestCase.unique_string())
        session_log = SessionLog(filepath=filepath)
        for tool_pose in self.tool_poses:
            session_log.append(tool_pose)

        with open(filepath, 'r') as session_log_file:
            tool_poses_yaml = load(session_log_file)
        for i, tool_pose in enumerate(self.tool_poses):
            self.assertTrue(tool_pose.tid in tool_poses_yaml[i])

            quaternion = tool_poses_yaml[i][tool_pose.tid]['quaternion']
            self.assertEqual(tool_pose.quaternion, quaternion)

            coordinates = tool_poses_yaml[i][tool_pose.tid]['coordinates']
            self.assertEqual(tool_pose.coordinates, coordinates)

            quality = tool_poses_yaml[i][tool_pose.tid]['quality']
            error = tool_poses_yaml[i][tool_pose.tid]['error']
            self.assertEqual(tool_pose.quality, (quality, error))

            timestamp = tool_poses_yaml[i][tool_pose.tid]['timestamp']
            self.assertEqual(tool_pose.timestamp, timestamp)

        print(open(filepath, 'r').read())
