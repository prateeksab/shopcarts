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


class Shopcart(db.Model):
    """
    Class that represents a Shopcart>
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    item_sku = db.Column(db.Integer, nullable=False)
    item_name = db.Column(db.String(260), nullable=False)
    item_quantity = db.Column(db.Integer, nullable=False)
    item_price = db.Column(db.Float, nullable=False)


    def __repr__(self):
        return "<Shopcart id=[%s] customer_id=[$s] item_name =[%s]>" % (self.id, self.customer_id, self.item_name)

    def create(self):
        """
        Creates a Shopcart to the database
        """
        logger.info("Creating Shopcart %s", self.id)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def save(self):
        """
        Updates a Shopcart to the database
        """
        logger.info("Saving %s", self.id)
        db.session.commit()

    def delete(self):
        """ Removes a Shopcart from the data store """
        logger.info("Deleting %s", self.id)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Shopcart into a dictionary """
        return {
            "id": self.id,
            "customer_id":self.customer_id,
            "item_sku":self.item_sku,
            "item_name":self.item_name,
            "item_quantity":self.item_quantity,
            "item_price":self.item_price
        }

    def deserialize(self, data):
        """
        Deserializes a Shopcart from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.id = data["id"]
            self.customer_id = data["customer_id"]
            self.item_sku = data["item_sku"]
            self.item_name = data["item_name"]
            self.item_quantity = data["item_quantity"]
            self.item_price = data["item_price"]

        except KeyError as error:
            raise DataValidationError(
                "Invalid Shopcart: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid Shopcart: body of request contained bad or no data"
            )
        return self

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
        """ Returns all of the Shopcarts in the database """
        logger.info("Processing all Shopcarts")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a Shopcart by its ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_or_404(cls, by_id):
        """ Find a Shopcart by its id """
        logger.info("Processing lookup or 404 for id %s ...", by_id)
        return cls.query.get_or_404(by_id)

    @classmethod
    def find_by_name(cls, item_name):
        """Returns all Shopcarts that has a specific item

        Args:
            name (string): the name of an item in a Shopcart you want to match
        """
        logger.info("Processing name query for %s ...", item_name)
        return cls.query.filter(cls.item_name == item_name)
