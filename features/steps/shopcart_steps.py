"""
Shopcarts feature testing

Steps file for Shopcart.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
from os import getenv
import logging
import json
import requests
from behave import *
from compare import expect, ensure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions

ID_PREFIX_1 = 'shopcart_'
ID_PREFIX_2 = 'item_'
empty = 'empty'


@given(u'the following shopcarts')
def step_impl(context):
    """ Delete all Shopcarts and load new ones """
    headers = {'Content-Type': 'application/json'}
    # list all of the shopcarts and delete them one by one
    context.resp = requests.get(context.base_url + '/shopcarts', headers=headers)
    expect(context.resp.status_code).to_equal(200)
    for shopcart in context.resp.json():
        context.resp = requests.delete(context.base_url + '/shopcarts/' + str(shopcart["id"]), headers=headers)
        expect(context.resp.status_code).to_equal(204)
    
    # load the database with new pets
    create_url = context.base_url + '/shopcarts'
    items_list = []
    for row in context.table:
        

        data = {
            "customer_id": row['customer_id'],
            "items_list": items_list
            }
        payload = json.dumps(data)
        context.resp = requests.post(create_url, data=payload, headers=headers)
        expect(context.resp.status_code).to_equal(201)



@when(u'I visit the "Home Page"')
def step_impl(context):
    """ Make a call to the base URL """
    context.driver.get(context.base_url)

@then(u'I should see "{message}" in the title')
def step_impl(context, message):
    """ Check the document title for a message """
    #message ="Shopcarts Demo RESTful Service"
    expect(context.driver.title).to_contain(message)
    


@then(u'I should not see "{message}"')
def step_impl(context,message):
    error_msg = "I should not see '%s' in '%s'" % (message, context.resp.text)
    ensure(message in context.resp.text, False, error_msg)
    
