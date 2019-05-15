import os
import sys

# When tests are run separately, Python doesn't recognize the other files in the package
# The lines below adds the projects base directory to path to work around this
projectdir = os.path.abspath(os.path.dirname(os.path.join('..', '..', "..")))
sys.path.append(projectdir)

import unittest
import config
from app import app
from app import models


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object(config.TestConfig)
        self.app = app.test_client()
        with app.app_context():
            models.db.init_app(app)
            models.db.create_all()

    def tearDown(self):
        with app.app_context():
            models.db.session.remove()
            models.db.drop_all()

    def test_product_table(self):
        with app.app_context():
            product = models.Product(name="Garri", description="Also known as cassava flakes")
            models.db.session.add(product)
            models.db.session.commit()
            result = models.Product.query.filter(models.Product.name == "Garri").first()
            self.assertEqual(result.description, "Also known as cassava flakes")

    def test_location_table(self):
        with app.app_context():
            location = models.Location(name="Lagos")
            models.db.session.add(location)
            models.db.session.commit()
            result = models.Location.query.filter(models.Location.id == 1).first()
            self.assertEqual(result.name, "Lagos")


if __name__ == '__main__':
    unittest.main()
