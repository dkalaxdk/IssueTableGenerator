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
