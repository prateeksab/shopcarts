# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for Shopcart Model
Test cases can be run with:
    nosetests
    coverage report -m
While debugging just these tests it's convinient to use this:
    nosetests --stop tests/test_models.py:TestShopcart
"""
import logging
import unittest
import os
from service.models import Shopcart, DataValidationError, db
from service import app
from .factories import ShopcartFactory

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
        fake_shopcart = ShopcartFactory()
        shopcart = Shopcart()
            #customer_id = fake_shopcart.customer_id
        self.assertTrue(shopcart != None)
        self.assertEqual(shopcart.id, None)

        self.assertTrue(fake_shopcart != None)
        self.assertEqual(fake_shopcart.id, 0)
        self.assertEqual(fake_shopcart.customer_id, 0)
        self.assertEqual(fake_shopcart.item_sku, 0)
        self.assertEqual(fake_shopcart.item_name, "item_dog")

        #self.assertEqual(shopcart.customer_id, fake_shopcart.customer_id)


    def test_add_item_to_shopcart(self):
        """ Add items to a shopcart, check that the items get added to database """
        shopcarts = Shopcart.all()
        shopcart = Shopcart(id=1,customer_id=1,item_sku=1,item_name="First Item", item_quantity=10,item_price=15)
        self.assertEqual(shopcarts, [])
        shopcart.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(shopcart.id, 1)
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)
