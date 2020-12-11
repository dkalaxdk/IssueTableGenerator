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


def list_to_csv(given_list):
    return ', '.join(given_list)


def convert_lists_to_csv(dict):
    new_dict = dict
    for key in new_dict:
        if type(new_dict[key]) is list:
            new_dict[key] = list_to_csv(new_dict[key])
    return new_dict
