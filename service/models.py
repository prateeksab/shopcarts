"""
Models for Shopcart

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass

######################################################################
#  P E R S I S T E N T   B A S E   M O D E L
######################################################################
class PersistentBase():
    """ Base class added persistent methods """

    def create(self):
        """
        Creates a Account to the database
        """
        logger.info("Creating %s", self.id)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def save(self):
        """
        Updates a Account to the database
        """
        logger.info("Saving %s", self.id)
        db.session.commit()

    def delete(self):
        """ Removes a Account from the data store """
        logger.info("Deleting %s", self.id)
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the records in the database """
        logger.info("Processing all records")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a record by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_or_404(cls, by_id):
        """ Find a record by it's id """
        logger.info("Processing lookup or 404 for id %s ...", by_id)
        return cls.query.get_or_404(by_id)

class Item(db.Model, PersistentBase):
    """
    Class that represents Items in a Shopcart>
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(260), nullable=False)
    item_quantity = db.Column(db.Integer, nullable=False)
    item_price = db.Column(db.Float, nullable=False)
    shopcart_id = db.Column(db.Integer, db.ForeignKey('shopcart.id'), nullable=False)

    def __repr__(self):
        return "<Shopcart id=[%s] customer_id=[%s] item_name =[%s]>" % (self.id, self.customer_id, self.item_name)

    def serialize(self):
        """ Serializes a Shopcart into a dictionary """
        return {
            "id": self.id,
            "item_name":self.item_name,
            "item_quantity":self.item_quantity,
            "item_price":self.item_price,
            "shopcart_id":self.shopcart_id
        }

    def deserialize(self, data):
        """
        Deserializes a Shopcart from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            # self.id = data["id"]
            self.item_name = data["item_name"]
            self.item_quantity = data["item_quantity"]
            self.item_price = data["item_price"]
            self.shopcart_id = data["shopcart_id"]

        except KeyError as error:
            raise DataValidationError(
                "Invalid Shopcart: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid Shopcart: body of request contained bad or no data"
            )
        return self

class Shopcart(db.Model, PersistentBase):

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    items_list = db.relationship('Item', backref='shopcart', lazy=True)  

    def __repr__(self):
        return "<Shopcart id=[%s] customer_id=[%s] item_name =[%s]>" % (self.id, self.customer_id, self.item_name)

    def serialize(self):
        """ Serializes a Shopcart into a dictionary """
        shopcart = {
            "id": self.id,
            "customer_id":self.customer_id,
            "items_list": []
        }
        for item in self.items_list:
            shopcart['items_list'].append(item.serialize())
        return shopcart

    def deserialize(self, data):
        """
        Deserializes a Shopcart from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            # self.id = data["id"]
            self.customer_id = data["customer_id"]
            # handle inner list of addresses
            self.items_list = data.get("items_list")
            for json_item in self.items_list:
                item = Item()
                item.deserialize(json_item)
                self.item.append(item)
        except KeyError as error:
            raise DataValidationError("Invalid Item: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Item: body of request contained" "bad or no data"
            )
        return self