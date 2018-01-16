import unittest
from pycontainerize.cli import main


class TestPyContainerize(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_help(self):
        try:
            main(['--help'])
        except SystemExit:
            self.assertTrue(True)
            return
        self.assertTrue(False)

    def test_subhelp(self):
        try:
            main(['gen', '--help'])
        except SystemExit:
            self.assertTrue(True)
            return
        self.assertTrue(False)

    def test_subsubhelp(self):
        try:
            main(['gen', 'create_project', '--help'])
        except SystemExit:
            self.assertTrue(True)
            return
        self.assertTrue(False)
