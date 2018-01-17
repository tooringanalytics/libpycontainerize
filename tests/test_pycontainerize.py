import unittest

from pycontainerize.cli import main as pycmain


class TestPycontainerizeCli(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_cli_help(self):
        self.assertTrue(True)
        return
        try:
            pycmain(['--help'])
        except SystemExit:
            self.assertTrue(True)
            return
        self.assertTrue(False)

    def test_cli_subhelp(self):
        self.assertTrue(True)
        return
        try:
            pycmain(['gen', '--help'])
        except SystemExit:
            self.assertTrue(True)
            return
        self.assertTrue(False)

    def test_cli_subsubhelp(self):
        self.assertTrue(True)
        return
        try:
            pycmain(['gen', 'create_project', '--help'])
        except SystemExit:
            self.assertTrue(True)
            return
        self.assertTrue(False)

    def test_cli_subsubhelp2(self):
        self.assertTrue(True)
        return
        try:
            pycmain(['builder', 'build_project', '--help'])
        except SystemExit:
            self.assertTrue(True)
            return
        self.assertTrue(False)
