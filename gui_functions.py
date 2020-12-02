def validate_input(data):
  # Check that all the values are formatted correctly
  # TODO Implement and test this function
  return True

def csvToList(string):
  string_without_wp = string.replace(" ", "")
  return string_without_wp.split(',')

def convert_csv_dict_items_to_lists(dict, dict_items):
  new_dict = dict
  for item in dict_items:
    new_dict[item] = csvToList(new_dict[item])
  return new_dict