from gui_functions import *

def test_validate_input():
  assert validate_input([])

def test_csv_to_list():
  assert csvToList('list, item, and, more') == ['list', 'item', 'and', 'more']
