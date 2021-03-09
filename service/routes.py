"""
My Service

Describe what your service does here
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status  # HTTP Status Codes

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import YourResourceModel, DataValidationError

# Import Flask application
from . import app

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    YourResourceModel.init_db(app)

def check_content_type(content_type):
    """ Checks that the media type is correct """
    if request.headers["Content-Type"] == content_type:
        return
    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(415, "Content-Type must be {}".format(content_type))


    #---------------------------------------------------------------------
#                C A R T  I T E M   M E T H O D S
#---------------------------------------------------------------------

######################################################################
# ADD AN ITEM TO A SHOPCART
######################################################################
@app.route('/shopcarts/<int:shopcart_id>/items', methods=['POST'])
def create_items(shopcart_id):
    """
    Create an Item in a Shopcart
    This endpoint will add an item to a shopcart
    """
    app.logger.info("Request to add an item to a shopcart")
    check_content_type("application/json")
    shopcart = ShopCart.find_or_404(shopcart_id)
    item = CartItem()
    item.deserialize(request.get_json())
    shopcart.items.append(item)
    shopcart.save()
    message = item.serialize()
    return make_response(jsonify(message), status.HTTP_201_CREATED)
