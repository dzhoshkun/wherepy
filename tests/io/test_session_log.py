import unittest
from os.path import (join, isfile)
from uuid import uuid4
from wherepy.io import SessionLog


class SessionLogTestCase(unittest.TestCase):

    @staticmethod
    def unique_string(length=6):
        return uuid4().hex[:length].upper()

    def test_invalid_filepath_raises(self):
        invalid_filepath = join('this', 'should-not', 'exist', 'session.yml')
        with self.assertRaises(OSError):
            SessionLog(filepath=invalid_filepath)

    def test_session_file_created(self):
        filepath = 'session-{}.yml'.format(SessionLogTestCase.unique_string())
        SessionLog(filepath=filepath)
        self.assertTrue(isfile(filepath))

    def test_tool_pose_appended_to_session_file(self):
        self.__fail()

    def __fail(self):
        self.fail('not implemented')
