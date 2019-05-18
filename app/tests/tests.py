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
            location = models.Location(name="Abroad", description="Not a warehouse")
            models.db.session.add(location)
            models.db.session.commit()

    def tearDown(self):
        with app.app_context():
            models.db.session.remove()
            models.db.drop_all()

    def test_home_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def test_products_page(self):
        response = self.app.get("/products")
        self.assertEqual(response.status_code, 200)

    def test_add_products_page(self):
        response = self.app.get("/products/add")
        self.assertEqual(response.status_code, 200)

    def test_products_can_be_added(self):
        self.app.post("/products/add", data={"name": "Garri", "description": "Also known as cassava flakes"})
        with app.app_context():
            result = models.Product.query.filter(models.Product.name == "Garri").first()
            self.assertEqual(result.description, "Also known as cassava flakes")

    def test_add_existing_product(self):
        self.app.post("/products/add", data={"name": "Garri", "description": "Also known as cassava flakes"})
        response = self.app.post("/products/add", data={"name": "Garri", "description": "Also known as cassava flakes"})
        self.assertIn("Product already exist", str(response.data))

    def test_edit_products_page(self):
        self.app.post("/products/add", data={"name": "Garri", "description": "Also known as cassava flakes"})
        response = self.app.get("/products/garri/edit")
        self.assertEqual(response.status_code, 200)

    def test_product_can_be_edited(self):
        self.app.post("/products/add", data={"name": "Garri", "description": "Also known as cassava flakes"})
        self.app.post("/products/garri/edit", data={"name": "Garri", "description": "Can be used for Eba"})
        with app.app_context():
            result = models.Product.query.filter(models.Product.name == "Garri").first()
            self.assertEqual(result.description, "Can be used for Eba")

    def test_edit_add_existing_product(self):
        self.app.post("/products/add", data={"name": "Rice", "description": "Oryza Sativa"})
        self.app.post("/products/add", data={"name": "Garri", "description": "Also known as cassava flakes"})
        response = self.app.post("/products/garri/edit", data={"name": "Rice", "description": "Oryza Sativa"})
        self.assertEqual(response.data, b"Error")

    def test_view_product_page(self):
        self.app.post("/products/add", data={"name": "Garri", "description": "Also known as cassava flakes"})
        response = self.app.get("/products/garri")
        self.assertEqual(response.status_code, 200)

    def test_view_false_product_page(self):
        response = self.app.get("/products/Another")
        self.assertEqual(response.status_code, 404)

    def test_locations_page(self):
        response = self.app.get("/locations")
        self.assertEqual(response.status_code, 200)

    def test_location_can_be_added(self):
        self.app.post("/locations/add", data={"name": "Lagos", "description": "Economic Capital of Nigeria"})
        with app.app_context():
            result = models.Location.query.filter(models.Location.name == "Lagos").first()
            self.assertEqual(result.description, "Economic Capital of Nigeria")

    def test_add_existing_location(self):
        self.app.post("/locations/add", data={"name": "Lagos", "description": "Economic Capital of Nigeria"})
        response = self.app.post("/locations/add", data={"name": "Lagos", "description": "Economic Capital of Nigeria"})
        self.assertEqual(response.data, b"Error")

    def test_edit_locations_page(self):
        self.app.post("/locations/add", data={"name": "Lagos", "description": "Economic Capital of Nigeria"})
        response = self.app.get("/locations/lagos/edit")
        self.assertEqual(response.status_code, 200)

    def test_locations_can_be_edited(self):
        self.app.post("/locations/add", data={"name": "Lagos", "description": "Economic Capital of Nigeria"})
        self.app.post("/locations/lagos/edit", data={"name": "Lagos", "description": "I no sabi Lagos"})
        with app.app_context():
            result = models.Location.query.filter(models.Location.name == "Lagos").first()
            self.assertEqual(result.description, "I no sabi Lagos")

    def test_edit_add_existing_location(self):
        self.app.post("/locations/add", data={"name": "Ibadan", "description": "Largest West Africa"})
        self.app.post("/locations/add", data={"name": "Lagos", "description": "Economic Capital of Nigeria"})
        response = self.app.post("/locations/lagos/edit", data={"name": "Ibadan", "description": "Largest West Africa"})
        self.assertEqual(response.data, b"Error")

    def test_view_location_page(self):
        self.app.post("/locations/add", data={"name": "Lagos", "description": "Economic Capital of Nigeria"})
        response = self.app.get("/locations/lagos")
        self.assertEqual(response.status_code, 200)

    def test_view_false_location_page(self):
        response = self.app.get("/locations/Another")
        self.assertEqual(response.status_code, 404)

    def test_movements(self):
        response = self.app.get("/product_movement")
        self.assertEqual(response.status_code, 200)

    def test_movements_can_be_made(self):
        product_name = "Garri"
        location_name = "Lagos"
        self.app.post("/products/add", data={"name": product_name, "description": "Also known as cassava flakes"})
        self.app.post("/locations/add", data={"name": location_name, "description": "Economic Capital of Nigeria"})
        with app.app_context():
            product_result = models.Product.query.filter(models.Product.name == product_name).first()
            product_id = product_result.id
            location_result = models.Location.query.filter(models.Location.name == location_name).first()
            location_id = location_result.id
        quantity = 10
        self.app.post("/movements", data={"to_location": location_id, "from_location": 1, "qty": quantity,
                                                 "description": "I need to move", "product": product_id})
        with app.app_context():
            mov_result = models.ProductMovement.query.filter(models.ProductMovement.product_id == product_id).first()
            self.assertEqual(mov_result.qty, quantity)

    def test_location_count(self):
        product_name = "Garri"
        location_name = "Lagos"
        self.app.post("/products/add", data={"name": product_name, "description": "Also known as cassava flakes"})
        self.app.post("/locations/add", data={"name": location_name, "description": "Economic Capital of Nigeria"})
        self.app.post("/locations/add", data={"name": "Ibadan", "description": "Largest in West Africa"})
        with app.app_context():
            product_result = models.Product.query.filter(models.Product.name == product_name).first()
            product_id = product_result.id
            location_result = models.Location.query.filter(models.Location.name == location_name).first()
            location_id = location_result.id
        quantity = 10
        self.app.post("/movements", data={"to_location": location_id, "from_location": 1, "qty": quantity,
                                                 "description": "I need to move", "product": product_id})

        self.app.post("/movements", data={"to_location": 3, "from_location": 2, "qty": 5,
                                                 "description": "I need to move too", "product": product_id})
        response = self.app.get("/locations/{}".format(location_name))
        self.assertEqual(response.data, b"{'Garri': 5}")

    def test_movements_impossible_quantity_size(self):
        product_name = "Garri"
        location_name = "Lagos"
        self.app.post("/products/add", data={"name": product_name, "description": "Also known as cassava flakes"})
        self.app.post("/locations/add", data={"name": location_name, "description": "Economic Capital of Nigeria"})
        self.app.post("/locations/add", data={"name": "Ibadan", "description": "Largest in West Africa"})
        with app.app_context():
            product_result = models.Product.query.filter(models.Product.name == product_name).first()
            product_id = product_result.id
            location_result = models.Location.query.filter(models.Location.name == location_name).first()
            location_id = location_result.id
        quantity = 10
        self.app.post("/movements", data={"to_location": location_id, "from_location": 1, "qty": quantity,
                                                 "description": "I need to move", "product": product_id})

        response = self.app.post("/movements", data={"to_location": 3, "from_location": 2, "qty": 15,
                                                            "description": "I need to move", "product": product_id})
        self.assertEqual(response.data, b"Error")


if __name__ == '__main__':
    unittest.main()
