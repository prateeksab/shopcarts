"""
Test cases for YourResourceModel Model

"""
import logging
import unittest
import os
from service.models import YourResourceModel, DataValidationError, db

######################################################################
#  <your resource name>   M O D E L   T E S T   C A S E S
######################################################################
class TestYourResourceModel(unittest.TestCase):
    """ Test Cases for YourResourceModel Model """

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
        pass

    def tearDown(self):
        """ This runs after each test """
        pass

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