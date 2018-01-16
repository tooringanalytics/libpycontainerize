import unittest
from pycontainerize.cli import main as pycmain


class TestPyContainerize(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_help(self):
        try:
            pycmain(['--help'])
        except SystemExit:
            self.assertTrue(True)
            return
        self.assertTrue(False)

    def test_subhelp(self):
        try:
            pycmain(['gen', '--help'])
        except SystemExit:
            self.assertTrue(True)
            return
        self.assertTrue(False)

    def test_subsubhelp(self):
        try:
            pycmain(['gen', 'create_project', '--help'])
        except SystemExit:
            self.assertTrue(True)
            return
        self.assertTrue(False)
