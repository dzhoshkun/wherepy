import unittest


class DummyTestCase(unittest.TestCase):

    def setUp(self):
        import wherepy.track
        self.package = wherepy.track

    def tearDown(self):
        self.package = None

    def test_can_import_package(self):
        self.assertTrue(False, 'Dummy assert statement')
