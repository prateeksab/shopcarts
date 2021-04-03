"""
My Service

Describe what your service does here
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status  # HTTP Status Codes
from werkzeug.exceptions import NotFound

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Shopcart, Item, DataValidationError

# Import Flask application
from . import app

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
            paths=url_for("list_shopcarts", _external=True),
        ),
        status.HTTP_200_OK
    )


######################################################################
# LIST ALL SHOPCARTS
######################################################################
@app.route("/shopcarts", methods=["GET"])
def list_shopcarts():
    """ Returns all of the Shopcart """
    app.logger.info("Request for Shopcart list")
    shopcarts = []
    shopcart_id = request.args.get("id")
    if shopcart_id:
        shopcarts = Shopcart.find_by_id(shopcart_id)
    else:
        shopcarts = Shopcart.all()

    results = [shopcart.serialize() for shopcart in shopcarts]
    return make_response(jsonify(results), status.HTTP_200_OK)

######################################################################
# RETRIEVE A SHOPCART
######################################################################
@app.route("/shopcarts/<int:id>", methods=["GET"])
def get_shopcarts(id):
    """
    Retrieve a single shopcart
    This endpoint will return a shopcart based on it's id
    """
    app.logger.info("Request for shopcart with id: %s", id)
    shopcart = Shopcart.find(id)
    if not shopcart:
        raise NotFound("Shopcart with id '{}' was not found.".format(id))
    return make_response(jsonify(shopcart.serialize()), status.HTTP_200_OK)


######################################################################
# ADD A NEW SHOP CART
######################################################################
@app.route("/shopcarts", methods=["POST"])
def create_shopcarts():
    """
    Creates a shopcart
    This endpoint will create a shopcart based the data in the body that is posted
    """
    app.logger.info("Request to create a shopcart")
    check_content_type("application/json")
    shopcart = Shopcart()
    shopcart.deserialize(request.get_json())
    shopcart.create()
    message = shopcart.serialize()
    location_url = url_for("get_shopcarts", id=shopcart.id, _external=True)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# ADD AN ITEM TO A SHOPCART
######################################################################
@app.route('/shopcarts/<int:shopcart_id>/items', methods=['POST'])
def create_items(shopcart_id):
    """
    Create an Item in an Shopcart
    This endpoint will add an item to a shopcart
    """
    app.logger.info("Request to add an item to a shopcart")
    check_content_type("application/json")
    shopcart = Shopcart.find_or_404(shopcart_id)
    item = Item()
    item.deserialize(request.get_json())
    shopcart.items_list.append(item)
    shopcart.save()
    message = item.serialize()
    return make_response(jsonify(message), status.HTTP_201_CREATED)

######################################################################
# RETRIEVE AN ITEM FROM SHOPCART
######################################################################
@app.route('/shopcarts/<int:shopcart_id>/items/<int:item_id>', methods=['GET'])
def get_items(shopcart_id, item_id):
    """
    Get an Item
    This endpoint returns just an item
    """
    app.logger.info("Request to get an item with id: %s", item_id)
    item = Item.find_or_404(item_id)
    return make_response(jsonify(item.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE A SHOPCART
######################################################################
@app.route("/shopcarts/<int:shopcart_id>", methods=["DELETE"])
def delete_shopcart(shopcart_id):
    """
    Delete a Shopcart
    This endpoint will delete an shopcart based the id specified in the path
    """
    app.logger.info("Request to delete shopcart with id: %s", shopcart_id)
    shopcart = Shopcart.find(shopcart_id)
    
    if shopcart:
        for item in shopcart.items_list:
            item_id = item.id
            delete_item(shopcart_id,item_id)
        shopcart.delete()
    return make_response("", status.HTTP_204_NO_CONTENT)



######################################################################
# DELETE AN ITEM
######################################################################
@app.route("/shopcarts/<int:shopcart_id>/items/<int:item_id>", methods=["DELETE"])
def delete_item(shopcart_id, item_id):
    """
    Delete an Item
    This endpoint will delete an Item based the id specified in the path
    """
    app.logger.info("Request to delete item with id: %s", shopcart_id)
    item = Item.find(item_id)
    if item:
        item.delete()
    return make_response("", status.HTTP_204_NO_CONTENT)





# RETRIEVE A SHOPCART
######################################################################
@app.route("/shopcarts/<int:shopcart_id>", methods=["GET"])
def get_shopcart(shopcart_id):
    """
    Retrieve a single Shopcart
    This endpoint will return a Shopcart based on it's id
    """
    app.logger.info("Request for shopcart with id: %s", shopcart_id)
    Shopcart = Shopcart.find_or_404(shopcart_id)
    return make_response(jsonify(Shopcart.serialize()), status.HTTP_200_OK)

######################################################################
# LIST ITEMS
######################################################################
@app.route("/shopcarts/<int:shopcart_id>/items", methods=["GET"])
def list_items(shopcart_id):
    """ Returns all of the Items for a Shopcart """
    app.logger.info("Request for Shopcart Items...")
    shopcart = Shopcart.find_or_404(shopcart_id)
    results = [item.serialize() for item in shopcart.items_list]
    return make_response(jsonify(results), status.HTTP_200_OK)

######################################################################
# UPDATE AN ITEM
######################################################################
@app.route("/shopcarts/<int:shopcart_id>/items/<int:item_id>", methods=["PUT"])
def update_items(shopcart_id, item_id):
    """
    Update a Shopcart
    This endpoint will update an Item based the body that is posted
    """
    app.logger.info("Request to update item with id: %s", item_id)
    check_content_type("application/json")
    item = Item.find_or_404(item_id)
    item.deserialize(request.get_json())
    item.id = item_id
    item.shopcart_id = shopcart_id
    item.save()
    return make_response(jsonify(item.serialize()), status.HTTP_200_OK)




######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Shopcart.init_db(app)

def check_content_type(content_type):
    """ Checks that the media type is correct """
    if request.headers["Content-Type"] == content_type:
        return
    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(415, "Content-Type must be {}".format(content_type))
