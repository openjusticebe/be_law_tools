# pylint: disable=function-redefined
from behave import when, given, then
import requests
from justel_lib import (
    justel_urls
)


@given(u'a set of parameters')
def step_impl(context):
    row = context.table[0]
    context.params = {
        'startDate': row['startDate'],
        'endDate': row['endDate'],
        'interval': row['interval']
    }


@when(u'I obtain the generator')
def step_impl(context):
    print(context.params)
    context.generator = justel_urls(**context.params)


@then(u'I can rotate through {loops:d} valid urls')
def step_impl(context, loops):
    i = 0
    for url in context.generator:
        i += 1
        r = requests.get(url)
        assert r.status_code == 200
    assert loops == i
