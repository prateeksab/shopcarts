from service import app
import os
import requests
from behave import given, when, then

@given(u'the server is started')
def step_impl(context):
    context.app = app.test_client()

@when(u'I visit the "home page"')
def step_impl(context):
    context.resp = context.app.get('/')

@then(u'I should see "{message}"')
def step_impl(context, message):
    assert message in str(context.resp.data)

@then(u'I should not see "{message}"')
def step_impl(context, message):
    assert message not in str(context.resp.data)