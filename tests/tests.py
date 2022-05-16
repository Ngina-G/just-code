import unittest
from app import create_app
from flask import current_app

class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('development')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):

        self.app_context.pop()
        self.app = None
        self.app_context = None

    def test_app_exists(self):
        self.assertFalse(current_app is None)
        assert current_app == self.app