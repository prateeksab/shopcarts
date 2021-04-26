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

###############################################################
##                                                           ##
##           IGNORE THE COMMENTED OUT SECTION                ##
##             CANNOT MAKE IT WORK, FOR NOW                  ##
##                                                           ##
###############################################################

    # Given the following shopcarts
    #     | id | customer_id |
    #     | 1  | 444         |
    #     | 2  | 555         |
    #     | 3  | 777         |

    # Given the following items
    #     | shopcart_id | id | item_name | item_quantity | item_price |
    #     | 1           | 1  | burger    | 3             | 2          |
    #     | 2           | 2  | toy       | 15            | 6.32       |
    #     | 3           | 3  | watch     | 2             | 195.30     |

    # @given(u"the following shopcarts")
# def step_impl(context):
#     """ list all of the shopcarts and delete them one by one """
#     headers = {"Content-Type": "application/json"}
#     context.resp = requests.get(context.base_url + '/shopcarts', headers=headers)
#     expect(context.resp.status_code).to_equal(200)
#     for shopcart in context.resp.json():
#         context.resp = requests.delete(context.base_url + '/shopcarts/' + str(shopcart["_id"]), headers=headers)
#         expect(context.resp.status_code).to_equal(204)
    
#     create_url = context.base_url + "/shopcarts"
#     for row in context.table:
#         data = {
#             "id": row["id"],
#             "customer_id": row["customer_id"],
#             "item_list": [],
#         }
#         payload = json.dumps(data)
#         context.resp = requests.post(create_url, data=payload, headers=headers)
#         expect(context.resp.status_code).to_equal(201)

# @given(u"the following items")
# def step_impl(context):
#     """ load new items deleted by given shopcarts """
#     headers = {"Content-Type": "application/json"}
#     create_url = context.base_url + "/shopcarts/"
    
#     for row in context.table:
#         data = {
#             "shopcart_id": row["shopcart_id"],
#             "id": row["id"],
#             "item_name": row["item_name"],
#             "item_quantity": row["item_quantity"],
#             "item_price": row["item_price"],
#         }
#         payload = json.dumps(data)
#         context.resp = requests.post(
#             create_url + row["shopcart_id"] + "/items" + row["id"], 
#             data=payload,
#             headers=headers,
#         )
#         expect(context.resp.status_code).to_equal(201)

# SERVER START
@given(u'there are no shopcarts')
def step_impl(context):
    headers = {'Content-Type': 'application/json'}
    # list all of the shopcarts and delete them one by one
    context.resp = requests.get(context.base_url + '/shopcarts', headers=headers)
    expect(context.resp.status_code).to_equal(200)
    for shopcart in context.resp.json():
        context.resp = requests.delete(context.base_url + '/shopcarts/' + str(shopcart["id"]), headers=headers)
        expect(context.resp.status_code).to_equal(204)

@when(u'I visit the "Home Page"')
def step_impl(context):
    context.driver.get(context.base_url)
    context.driver.save_screenshot('homepage_check.png')

@then(u'I should see "{message}"')
def step_impl(context, message):
    expect(context.driver.title).to_contain(message)

@then(u'I should not see "{message}"')
def step_impl(context, message):
    error_msg = 'I should not see "%s" in "%s"' % (message, context.driver.title)
    ensure(message in context.driver.title, False, error_msg)

@when(u'I set the "{element_name}" field to "{text_string}"')
def step_impl(context, element_name, text_string):
    # context.driver.save_screenshot('debug.png')
    element_id = element_name.lower()
    element = context.driver.find_element_by_id(element_id)
    element.clear()
    element.send_keys(text_string)

@when(u'I press the "{button}" button')
def step_impl(context, button):
    button_id = button.lower() + '-btn'
    context.driver.find_element_by_id(button_id).click()

@then(u'I should see the message "{message}"')
def step_impl(context, message):
    found = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'flash_message'),
            message
        )
    )
    expect(found).to_be(True)

##################################################################
# These two function simulate copy and paste
##################################################################
@when(u'I copy the "{element_name}" field')
def step_impl(context, element_name):
    element_id = element_name.lower()
    # element = context.driver.find_element_by_id(element_id)
    element = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    context.clipboard = element.get_attribute('value')
    logging.info('Clipboard contains: %s', context.clipboard)

@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    element_id = element_name.lower()
    # element = context.driver.find_element_by_id(element_id)
    element = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(context.clipboard)

@then(u'the "{element_name}" field should be empty')
def step_impl(context, element_name):
    element_id = element_name.lower()
    element = context.driver.find_element_by_id(element_id)
    expect(element.get_attribute('value')).to_be(u'')