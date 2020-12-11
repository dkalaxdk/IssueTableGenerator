from helpers.filter_functions import *
from classes.pull_requests import *


def test_string_contains_word_false():
    title = "Something something Testing"
    words = ["Another"]
    assert not string_contains_word(title, words)


def test_string_contains_word_true():
    title = "Something something Testing"
    words = ["Something"]
    assert string_contains_word(title, words)
