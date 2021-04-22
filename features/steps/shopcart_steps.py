# import os
# import requests
# from behave import given, when, then

import os
import logging
import json
import requests
from behave import *
from compare import expect, ensure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions
from service import app


# SERVER START

@given(u'the server is started')
def step_impl(context):
    context.app = app.test_client()

@when(u'I visit the "Home Page"')
def step_impl(context):
    context.resp = context.app.get('/')

@then(u'I should see "{message}"')
def step_impl(context, message):
    assert message in str(context.resp.data)

@then(u'I should not see "{message}"')
def step_impl(context, message):
    assert message not in str(context.resp.data)

# ADD AN ITEM TO A SHOPCART
@when(u'I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, element_name.lower()))
    )
    element.clear()
    element.send_keys(text_string)


    # WebDriverWait()
    # element = context.driver.find_element_by_id(element_name.lower())
    # element.clear()
    # element.send_keys(text_string)
    # raise NotImplementedError(u'STEP: When I set the "Customer ID" to "2020"')

# @when(u'I press the "Create Shopcart" button')
# def step_impl(context):
#     raise NotImplementedError(u'STEP: When I press the "Create Shopcart" button')


# @when(u'I set "Shopcart ID" to "1"')
# def step_impl(context):
#     raise NotImplementedError(u'STEP: When I set "Shopcart ID" to "1"')


# @then(u'I should see the message "Successfully created the shopcart for customer: 2020. Shopcart ID is 1"')
# def step_impl(context):
#     raise NotImplementedError(u'STEP: Then I should see the message "Successfully created the shopcart for customer: 2020. Shopcart ID is 1"')


# @then(u'I press the "Retrieve Shopcart" button')
# def step_impl(context):
#     raise NotImplementedError(u'STEP: Then I press the "Retrieve Shopcart" button')


# @then(u'I set "Item ID" to "100001"')
# def step_impl(context):
#     raise NotImplementedError(u'STEP: Then I set "Item ID" to "100001"')


# @then(u'I set "Item Name" to "Hungry Hippos"')
# def step_impl(context):
#     raise NotImplementedError(u'STEP: Then I set "Item Name" to "Hungry Hippos"')


# @then(u'I set "Item Quantity" to "25"')
# def step_impl(context):
#     raise NotImplementedError(u'STEP: Then I set "Item Quantity" to "25"')


# @then(u'I set "Item Price" to "99.99"')
# def step_impl(context):
#     raise NotImplementedError(u'STEP: Then I set "Item Price" to "99.99"')


# @then(u'I press the "Add Item to cart" button')
# def step_impl(context):
#     raise NotImplementedError(u'STEP: Then I press the "Add Item to cart" button')


# @then(u'I should see the message "Success: Added the item Hungry Hippos shopcart 1"')
# def step_impl(context):
#     raise NotImplementedError(u'STEP: Then I should see the message "Success: Added the item Hungry Hippos shopcart 1"')