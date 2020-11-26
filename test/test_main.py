from main import *

def test_unique_list_function():
  assert isinstance(unique_list_function([], 'string'), list) == True, 'unique_list_function should return a list'