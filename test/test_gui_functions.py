from gui_functions import *

def test_validate_input():
  assert validate_input([])

def test_csv_to_list():
  assert csvToList('list, item, and, more') == ['list', 'item', 'and', 'more']

def test_convert_csv_dict_items_to_lists():
  testDict = {
    'item1': '1, 2, 3',
    'item2': 'not a list',
    'item3': 'string1, string2'
  }

  expected = {
    'item1': ['1', '2', '3'],
    'item2': 'not a list',
    'item3': ['string1', 'string2']
  }

  actual = convert_csv_dict_items_to_lists(testDict, ['item1', 'item3'])

  assert actual == expected

def test_list_to_csv():
  assert list_to_csv(['one', 'two', 'three']) == 'one, two, three'

def test_convert_lists_to_csv():
  test_dict = {
    'list_item': ['one', 'two', 'three'],
    'not_list_item': 'hello'
  }

  expected = {
    'list_item': 'one, two, three',
    'not_list_item': 'hello'
  }

  assert convert_lists_to_csv(test_dict) == expected

