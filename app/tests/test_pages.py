import os
import sys

# When tests are run separately, Python doesn't recognize the other files in the package
# The lines below adds the projects base directory to path to work around this
projectdir = os.path.abspath(os.path.dirname(os.path.join('..', '..', "..")))
sys.path.append(projectdir)

import unittest
import config
from app import app


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object(config.TestConfig)
        self.app = app.test_client()

    def test_home(self):
        result = self.app.get("/")
        self.assertEqual(result.status_code, 200)

    def test_products(self):
        result = self.app.get("/products")
        self.assertEqual(result.status_code, 200)

    def test_locations(self):
        result = self.app.get("/locations")
        self.assertEqual(result.status_code, 200)

    def test_movements(self):
        result = self.app.get("/movements")
        self.assertEqual(result.status_code, 200)


if __name__ == '__main__':
    unittest.main()
