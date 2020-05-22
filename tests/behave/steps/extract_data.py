# pylint: disable=function-redefined
import requests
import time
from bs4 import BeautifulSoup as bs
from behave import when, given, then
from justel_lib import (
    soup2meta
)


@given(u'justel uri "{uri}"')
def step_impl(context, uri):
    context.uri = uri


@when(u'I download the document')
def step_impl(context):
    while True:
        url = f"http://www.ejustice.just.fgov.be/eli/{context.uri}"
        r = requests.get(url, allow_redirects=False)
        if r.status_code == 200:
            break
        time.sleep(2)
    context.document = r.text
    context.soup = bs(r.text, 'html5lib')


@when(u'I extract meta data')
def step_impl(context):
    context.meta = soup2meta(context.soup)


@then(u'I find a document number')
def step_impl(context):
    assert 'number' in context.meta


@then(u'the document "{key}" is "{value}"')
def step_impl(context, key, value):
    assert context.meta[key] == value


@then(u'it updated {num:d} other documents')
def step_impl(context, num):
    assert len(context.meta['updated']) == num


