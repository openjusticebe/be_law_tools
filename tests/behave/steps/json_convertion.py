# pylint: disable=function-redefined
from behave import when, given, then
from justel_lib import (
    extract_data
)
from justel2json import (
    text2dict_arr,
    dict_arr2tree
)


@when(u'I extract unformatted data')
def step_impl(context):
    context.main_text,context.meta = extract_data(context.uri)

@when(u'I convert to dict')
def step_impl(context):
    context.dict = text2dict_arr(context.main_text, context.meta["language"])


@then(u'It contains the type "{typeC}" with reference "{ref}" at position {pos:d}')
def step_impl(context, typeC, ref, pos):
    assert context.dict[pos]["type"] == typeC
    assert context.dict[pos]["ref"] == ref

@then(u'It contains at least {number_of_entries:d} entries')
def step_impl(context, number_of_entries):
    assert len(context.dict) > number_of_entries


@when(u'I convert dict to tree')
def step_impl(context):
    context.tree = dict_arr2tree(context.dict)


@then(u'there is {num:d} root children')
def step_impl(context, num):
    assert len(context.tree["children"]) == num

@then(u'the first children is of type "{typeC}"')
def step_impl(context, typeC):
    assert context.tree["children"][0]["type"] == typeC

