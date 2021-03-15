"""
TestShopcart API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from flask_api import status  # HTTP Status Codes
from service.models import db
from service.routes import app, init_db
from .factories import ShopcartFactory

######################################################################
#  T E S T   C A S E S
######################################################################
class TestYourResourceServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        pass

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        self.app = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        pass
    
    def _create_shopcarts(self, count):
        """ Factory method to create shopcarts in bulk """
        carts = []
        for _ in range(count):
            test_cart = ShopcartFactory()
            resp = self.app.post(
                "/pets", json=test_cart.serialize(), content_type="application/json"
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test shopcart"
            )
            new_cart = resp.get_json()
            test_cart.id = new_cart["id"]
            carts.append(test_cart)
        return carts

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ Test index call """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
    
    def test_create_shopcart(self):
        """ Create a new shopcart """
        test_cart = ShopcartFactory()
        logging.debug(test_cart)
        resp = self.app.post(
            "/shopcarts", json=test_cart.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        # Check the data is correct
        new_cart = resp.get_json()
        #self.assertEqual(new_cart["id"], test_cart.id, "IDs do not match")
        self.assertEqual(
            new_cart["customer_id"], test_cart.customer_id, "Customer IDs do not match"
        )
        self.assertEqual(
            new_cart["item_sku"], test_cart.item_sku, "Item SKU does not match"
        )
        self.assertEqual(
            new_cart["item_name"], test_cart.item_name, "Item names do not match"
        )
        self.assertEqual(
            new_cart["item_quantity"], test_cart.item_quantity, "Item quantity does not match"
        )
        self.assertEqual(
            new_cart["item_price"], test_cart.item_price, "Item Price does not match"
        )
        # Check that the location header was correct
        resp = self.app.get(location, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_cart = resp.get_json()
       #self.assertEqual(new_cart["id"], test_cart.id, "IDs do not match")
        self.assertEqual(
            new_cart["customer_id"], test_cart.customer_id, "Customer IDs do not match"
        )
        self.assertEqual(
            new_cart["item_sku"], test_cart.item_sku, "Item SKU does not match"
        )
        self.assertEqual(
            new_cart["item_name"], test_cart.item_name, "Item names do not match"
        )
        self.assertEqual(
            new_cart["item_quantity"], test_cart.item_quantity, "Item quantity does not match"
        )
        self.assertEqual(
            new_cart["item_price"], test_cart.item_price, "Item Price does not match"
        )