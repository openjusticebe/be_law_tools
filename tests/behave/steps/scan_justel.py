# pylint: disable=function-redefined
# flake8: noqa=F811
from behave import when, given, then
import requests
from justel_lib import (
    justel_urls,
    justel_eli_scan,
    justel_doc_scan,
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
    context.generator = justel_urls(**context.params)


@then(u'I can rotate through {loops:d} valid urls')
def step_impl(context, loops):
    i = 0
    for url in context.generator:
        i += 1
        r = requests.get(url)
        assert r.status_code == 200
    assert loops == i


@given(u'some page urls')
def step_impl(context):
    context.params = []
    for row in context.table:
        context.params.append({
            'url': row['url'],
            'result': True if row['result'] == 'True' else False,
            'links': int(row['links'])
        })


@when(u'I feed them to the page scanner')
def step_impl(context):
    context.results = {}
    for row in context.params:
        result, links = justel_eli_scan(row['url'])
        context.results[hash(row['url'])] = {
            'result': result,
            'links': links
        }


@then(u'I obtain the expected results')
def step_impl(context):
    for row in context.params:
        res = context.results[hash(row['url'])]
        print('--')
        print(row)
        print(res)
        assert row['result'] == res['result']


@then(u'I obtain the expected link count')
def step_impl(context):
    for row in context.params:
        res = context.results[hash(row['url'])]
        assert row['links'] == len(res['links'])


@given(u'some document urls')
def step_impl(context):
    context.params = []
    for row in context.table:
        context.params.append({
            'url': row['url'],
            'result': True if row['result'] == 'True' else False,
            'text_length': int(row['text_length'])
        })


@when(u'I feed them to the document scanner')
def step_impl(context):
    context.results = {}
    for row in context.params:
        result, text = justel_doc_scan(row['url'])
        context.results[hash(row['url'])] = {
            'result': result,
            'text_length': len(text)
        }


@then(u'I obtain the expected text length')
def step_impl(context):
    for row in context.params:
        res = context.results[hash(row['url'])]
        assert row['text_length'] == res['text_length']

