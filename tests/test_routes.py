"""
TestShopcart API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
import unittest
from flask_api import status  # HTTP Status Codes
from tests.factories import ShopcartFactory, ItemFactory
from service.models import db
from service.routes import app, init_db

# DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

BASE_URL = '/shopcarts'
CONTENT_TYPE_JSON = "application/json"

######################################################################
#  T E S T   C A S E S
######################################################################
class TestShopcartServer(unittest.TestCase):
    """ Shopcart Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.debug = False
        app.testing = True
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        init_db()

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

######################################################################
#  H E L P E R   M E T H O D S
######################################################################

    def _create_shopcarts(self, count):
        """ Factory method to create shopcarts in bulk """
        shopcarts = []
        for _ in range(count):
            shopcart = ShopcartFactory()
            resp = self.app.post(
                BASE_URL, json=shopcart.serialize(), content_type=CONTENT_TYPE_JSON
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test Shopcart"
            )
            new_shopcart = resp.get_json()
            shopcart.id = new_shopcart["id"]
            shopcarts.append(shopcart)
        return shopcarts

######################################################################
#  P L A C E   T E S T   C A S E S   H E R E
######################################################################

    def test_index(self):
        """ Test index call """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], "Shopcart REST API Service")
    
    def test_create_shopcart(self):
        """ Create a new Shopcart """
        shopcart = ShopcartFactory()
        resp = self.app.post(
            BASE_URL, 
            json=shopcart.serialize(), 
            content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        
        # Check the data is correct
        new_shopcart = resp.get_json()
        self.assertEqual(new_shopcart["id"], shopcart.id, "ID does not match")
        self.assertEqual(new_shopcart["customer_id"], shopcart.customer_id, "CUSTOMER_ID does not match")

        # Check that the location header was correct by getting it
        resp = self.app.get(location, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_shopcart = resp.get_json()
        self.assertEqual(new_shopcart["id"], shopcart.id, "ID does not match")
        self.assertEqual(new_shopcart["customer_id"], shopcart.customer_id, "CUSTOMER_ID does not match")

    # def test_create_shopcart(self):
    #     """ Create a new shopcart """
    #     test_shopcart = ShopcartFactory()
    #     logging.debug(test_shopcart)
    #     resp = self.app.post(
    #         BASE_URL, json=test_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
    #     )
    #     self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
    #     # Make sure location header is set
    #     location = resp.headers.get("Location", None)
    #     self.assertIsNotNone(location)
    #     # Check the data is correct
    #     new_shopcart = resp.get_json()
    #     self.assertEqual(new_shopcart["id"], test_shopcart.id, "IDs do not match")
    #     self.assertEqual(
    #         new_shopcart["customer_id"], test_shopcart.customer_id, "Customer IDs do not match"
    #     )
    #     self.assertEqual(
    #         new_shopcart["item_sku"], test_shopcart.item_sku, "Item SKU does not match"
    #     )
    #     self.assertEqual(
    #         new_shopcart["item_name"], test_shopcart.item_name, "Item names do not match"
    #     )
    #     self.assertEqual(
    #         new_shopcart["item_quantity"], test_shopcart.item_quantity, "Item quantity does not match"
    #     )
    #     self.assertEqual(
    #         new_shopcart["item_price"], test_shopcart.item_price, "Item Price does not match"
    #     )
    #     # Check that the location header was correct
    #     resp = self.app.get(location, content_type=CONTENT_TYPE_JSON)
    #     self.assertEqual(resp.status_code, status.HTTP_200_OK)
    #     new_shopcart = resp.get_json()
    #     self.assertEqual(new_shopcart["id"], test_shopcart.id, "IDs do not match")
    #     self.assertEqual(
    #         new_shopcart["customer_id"], test_shopcart.customer_id, "Customer IDs do not match"
    #     )
    #     self.assertEqual(
    #         new_shopcart["item_sku"], test_shopcart.item_sku, "Item SKU does not match"
    #     )
    #     self.assertEqual(
    #         new_shopcart["item_name"], test_shopcart.item_name, "Item names do not match"
    #     )
    #     self.assertEqual(
    #         new_shopcart["item_quantity"], test_shopcart.item_quantity, "Item quantity does not match"
    #     )
    #     self.assertEqual(
    #         new_shopcart["item_price"], test_shopcart.item_price, "Item Price does not match"
    #     )