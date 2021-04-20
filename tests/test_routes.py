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
        resp = self.app.get("/api")
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
        self.assertEqual(new_shopcart["customer_id"], shopcart.customer_id, "CUSTOMER_ID does not match")

        # Check that the location header was correct by getting it
        resp = self.app.get(location, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_shopcart = resp.get_json()
        self.assertEqual(new_shopcart["customer_id"], shopcart.customer_id, "CUSTOMER_ID does not match")

    def test_add_item(self):
        """ Add an item to a shopcart """
        shopcart = self._create_shopcarts(1)[0]
        item = ItemFactory()
        resp = self.app.post(
            "/shopcarts/{}/items".format(shopcart.id), 
            json=item.serialize(), 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["shopcart_id"], shopcart.id)
        self.assertIsNotNone(data["id"])
        self.assertEqual(data["item_name"], item.item_name)
        self.assertEqual(data["item_quantity"], item.item_quantity)
        self.assertEqual(data["item_price"], item.item_price)

    def test_checkout_shopcart(self):
        """ Checkout a Shopcart REAL """
        shopcart = self._create_shopcarts(1)[0]
        item = ItemFactory()
        resp = self.app.post(
            "/shopcarts/{}/items".format(shopcart.id), 
            json=item.serialize(), 
            content_type=CONTENT_TYPE_JSON
            )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        resp2 = self.app.put(
            "/shopcarts/{}".format(shopcart.id), 
            json=item.serialize(), 
            content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp2.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_item_list(self):
        """ Get a list of Items """
        self._create_items(5)
        resp = self.app.get("/items")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_get_shopcart_list(self):
        """ Get a list of shopcarts """
        self._create_shopcarts(5)
        resp = self.app.get("/shopcarts")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)        

    def test_get_shopcart(self):
        """ Get a single Shopcart by ID """
        shopcart = self._create_shopcarts(2)[0]
        resp = self.app.get(
            "/shopcarts/{}".format(shopcart.id), 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["id"], shopcart.id)
    
    def test_get_item_list(self):
        """ Get an item from a shopcart """
        # create a known item
        shopcart = self._create_shopcarts(1)[0]
        item = ItemFactory()
        resp = self.app.post(
            "/shopcarts/{}/items".format(shopcart.id), 
            json=item.serialize(), 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        data = resp.get_json()
        logging.debug(data)
        shopcart_id = data["id"]

        # retrieve it back
        resp = self.app.get(
            "/shopcarts/{}/items".format(shopcart.id), 
            content_type="application/json" 
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        logging.debug(data)

    def test_update_item(self):
        """ Update an item on an shopcart """
        # create a known item
        shopcart = self._create_shopcarts(1)[0]
        item = ItemFactory()
        resp = self.app.post(
            "/shopcarts/{}/items".format(shopcart.id), 
            json=item.serialize(), 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        data = resp.get_json()
        logging.debug(data)
        item_id = data["id"]
        data["item_name"] = "XXXX"

        # send the update back
        resp = self.app.put(
            "/shopcarts/{}/items/{}".format(shopcart.id, item_id), 
            json=data, 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # retrieve it back
        resp = self.app.get(
            "/shopcarts/{}/items/{}".format(shopcart.id, item_id), 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["id"], item_id)
        self.assertEqual(data["shopcart_id"], shopcart.id)
        self.assertEqual(data["item_name"], "XXXX")

    def test_delete_item(self):
        """ Delete an item """
        shopcart = self._create_shopcarts(1)[0]
        item = ItemFactory()
        resp = self.app.post(
            "/shopcarts/{}/items".format(shopcart.id), 
            json=item.serialize(), 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        logging.debug(data)
        item_id = data["id"]

        # send delete request
        resp = self.app.delete(
            "/shopcarts/{}/items/{}".format(shopcart.id, item_id),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        # retrieve it back and make sure item is not there
        resp = self.app.get(
            "/shopcarts/{}/items/{}".format(shopcart.id, item_id), 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)


    def test_delete_shopcart(self):
        """ Delete a shopcart """
        shopcart = self._create_shopcarts(1)[0]
        item = ItemFactory()
        resp = self.app.post(
            "/shopcarts/{}/items".format(shopcart.id), 
            json=item.serialize(), 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        logging.debug(data)
        item_id = data["id"]

        # send delete request
        resp = self.app.delete(
            "/shopcarts/{}".format(shopcart.id),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        # retrieve it back and make sure item is not there
        # resp = self.app.get(
        #     "/shopcarts/{}/items/{}".format(shopcart.id, item_id), 
        #     content_type="application/json"
        # )
        # self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_unsupported_media_type(self):
        """ Send wrong media type """
        shopcart = ShopcartFactory()
        resp = self.app.post(
            "/shopcarts", 
            json=shopcart.serialize(), 
            content_type="test/html"
        )
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    
    def test_method_not_allowed(self):
        """ Make an illegal method call """
        resp = self.app.put(
            "/shopcarts", 
            json={"not": "today"}, 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_bad_request(self):
        """ Send wrong media type """
        shopcart = ShopcartFactory()
        resp = self.app.post(
            "/shopcarts", 
            json={"name": "not enough data"}, 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)