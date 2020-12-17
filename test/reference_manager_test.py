from helpers.reference_manager import *


class TestClass:
    def __init__(self, element):
        self.element = element


def test_return_list_number_number_in_list():
    query = "One"
    object_property = "element"
    input_list = [TestClass("One"), TestClass("Two"), TestClass("Three")]
    assert return_list_number(input_list, object_property, query) == 0


def test_return_list_number_number_not_in_list():
    query = "Four"
    object_property = "element"
    input_list = [TestClass("One"), TestClass("Two"), TestClass("Three")]
    assert return_list_number(input_list, object_property, query) == -1


def test_return_list_number_element_does_not_contain_property():
    query = "Four"
    object_property = "TESTELEMENT"
    input_list = [TestClass("One"), TestClass("Two"), TestClass("Three")]
    assert return_list_number(input_list, object_property, query) == -2
