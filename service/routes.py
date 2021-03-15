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
from service.models import Shopcart, DataValidationError

# Import Flask application
from . import app
from werkzeug.exceptions import NotFound

######################################################################
# Error Handlers
######################################################################
@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    return bad_request(error)


@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(error):
    """ Handles bad reuests with 400_BAD_REQUEST """
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(
            status=status.HTTP_400_BAD_REQUEST, error="Bad Request", message=message
        ),
        status.HTTP_400_BAD_REQUEST,
    )


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    """ Handles resources not found with 404_NOT_FOUND """
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(status=status.HTTP_404_NOT_FOUND, error="Not Found", message=message),
        status.HTTP_404_NOT_FOUND,
    )


@app.errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
def method_not_supported(error):
    """ Handles unsuppoted HTTP methods with 405_METHOD_NOT_SUPPORTED """
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
            error="Method not Allowed",
            message=message,
        ),
        status.HTTP_405_METHOD_NOT_ALLOWED,
    )


@app.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
def mediatype_not_supported(error):
    """ Handles unsuppoted media requests with 415_UNSUPPORTED_MEDIA_TYPE """
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(
            status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            error="Unsupported media type",
            message=message,
        ),
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    )


@app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    """ Handles unexpected server error with 500_SERVER_ERROR """
    message = str(error)
    app.logger.error(message)
    return (
        jsonify(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error="Internal Server Error",
            message=message,
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
        jsonify(
            name="Shopcart REST API Service",
            version="1.0",
            
        ),
        status.HTTP_200_OK,
    )




######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Shopcart.init_db(app)


######################################################################
# RETRIEVE A SHOPCART
######################################################################
@app.route("/shopcarts/<int:pet_id>", methods=["GET"])
def get_shopcarts(id):
    """
    Retrieve a single shopcart
    This endpoint will return a shopcart based on it's id
    """
    app.logger.info("Request for shopcart with id: %s", id)
    shopcart = Shopcart.find(id)
    if not shopcart:
        raise NotFound("Pet with id '{}' was not found.".format(id))
    return make_response(jsonify(shopcart.serialize()), status.HTTP_200_OK)


######################################################################
# ADD A NEW SHOP CART
######################################################################
@app.route("/shopcart", methods=["POST"])
def create_shopcarts():
    """
    Creates a shopcart
    This endpoint will create a shopcart based the data in the body that is posted
    """
    app.logger.info("Request to create a shopcart")
    #check_content_type("application/json")
    shopcart = Shopcart()
    shopcart.deserialize(request.get_json())
    shopcart.create()
    message = shopcart.serialize()
    location_url = url_for("get_shopcarts", id=shopcart.id, _external=True)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )


# @app.route('/shopcarts/<int:shopcart_id>/items', methods=['POST'])
# def create_items(shopcart_id):
#     """
#     Create an Item in a Shopcart
#     This endpoint will add an item to a shopcart
#     """
#     app.logger.info("Request to add an item to a shopcart")
#     check_content_type("application/json")
#     shopcart = Shopcart.find_or_404(shopcart_id)
#     #item = CartItem()
#     item.deserialize(request.get_json())
#     shopcart.items.append(item)
#     shopcart.save()
#     message = item.serialize()
#     return make_response(jsonify(message), status.HTTP_201_CREATED)
