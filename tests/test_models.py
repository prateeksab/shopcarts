"""
Test cases for Shopcart Model

"""
import logging
import unittest
import os
from service.models import Shopcart, DataValidationError, db
from service import app

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  S H O P C A R T    M O D E L   T E S T   C A S E S
######################################################################
class TestShopcart(unittest.TestCase):
    """ Test Cases for Shopcart Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Shopcart.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_XXXX(self):
        """ Test something """
        self.assertTrue(True)


    def test_create_shopcart(self):
        """ Create a ShopCart -- Asserts that it exists """
        fake_shopcart = ShopCartFactory()
        shopcart = ShopCart(
            customer_id = fake_shopcart.customer_id
        )
        self.assertTrue(shopcart != None)
        self.assertEqual(shopcart.id, None)
        self.assertEqual(shopcart.customer_id, fake_shopcart.customer_id)


    def test_add_shopcart(self):
        """ Create a ShopCart -- Add it to the database """
        shopcarts = ShopCart.all()
        self.assertEqual(shopcarts, [])
        shopcart = self._create_shopcart()
        shopcart.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(shopcart.id, 1)
        shopcarts = ShopCart.all()
        self.assertEqual(len(shopcarts), 1)
