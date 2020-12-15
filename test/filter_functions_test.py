from helpers.filter_functions import *
from classes.pull_requests import *
from classes.issues import *


def test_string_contains_word_false():
    title = "Something something Testing"
    words = ["Another"]
    assert not string_contains_word(title, words)


def test_string_contains_word_true():
    title = "Something something Testing"
    words = ["Something"]
    assert string_contains_word(title, words)


def test_issue_in_milestone_return_true():
    test_issue = Issue()
    test_issue.milestone = "milestone"
    config = {"milestone": "milestone"}
    assert issue_in_milestone(test_issue, config)


def test_issue_in_milestone_return_false():
    test_issue = Issue()
    test_issue.milestone = "milestone"
    config = {"milestone": "test_milestone"}
    assert not issue_in_milestone(test_issue, config)


def test_contains_correct_labels_returns_true():
    config = {"required_labels": ["Label one"]}
    test_issue = Issue()
    label_one = Label()
    label_two = Label()
    label_one.name = "Label one"
    label_two.name = "Label two"
    test_issue.labels = [label_one, label_two]
    assert contains_correct_labels(config, test_issue)


def test_contains_correct_labels_returns_true_empty_element():
    config = {"required_labels": [""]}
    test_issue = Issue()
    label_one = Label()
    label_two = Label()
    label_one.name = "Label one"
    label_two.name = "Label two"
    test_issue.labels = [label_one, label_two]
    assert contains_correct_labels(config, test_issue)


def test_contains_correct_labels_returns_false():
    config = {"required_labels": ["Label one"]}
    test_issue = Issue()
    label_one = Label()
    label_two = Label()
    label_one.name = "Label test"
    label_two.name = "Label two"
    test_issue.labels = [label_one, label_two]
    assert not contains_correct_labels(config, test_issue)


def test_contains_correct_labels_returns_true_no_required_labels():
    config = {"required_labels": []}
    test_issue = Issue()
    label_one = Label()
    label_two = Label()
    label_one.name = "Label test"
    label_two.name = "Label two"
    test_issue.labels = [label_one, label_two]
    assert contains_correct_labels(config, test_issue)


def test_date_time_check_return_true_from_date_set():
    test_date = "2020-04-25T08:24:19Z"
    config = {"from_date": "2020-04-21",
              "to_date": ""}
    assert date_time_check(test_date, config)


def test_date_time_check_return_true_to_date_set():
    test_date = "2020-04-25T08:24:19Z"
    config = {"from_date": "",
              "to_date": "2020-05-21"}
    assert date_time_check(test_date, config)


def test_date_time_check_return_false_to_date_set():
    test_date = "2020-04-25T08:24:19Z"
    config = {"from_date": "",
              "to_date": "2020-03-21"}
    assert not date_time_check(test_date, config)


def test_date_time_check_return_false_from_date_set():
    test_date = "2020-04-25T08:24:19Z"
    config = {"from_date": "2020-06-21",
              "to_date": ""}
    assert not date_time_check(test_date, config)


def test_date_time_check_return_false_both_date_set():
    test_date = "2020-07-25T08:24:19Z"
    config = {"from_date": "2020-06-21",
              "to_date": "2020-06-21"}
    assert not date_time_check(test_date, config)


def test_date_time_check_return_true_both_date_set():
    test_date = "2020-07-25T08:24:19Z"
    config = {"from_date": "2020-04-21",
              "to_date": "2020-08-21"}
    assert date_time_check(test_date, config)


def test_date_time_check_return_true_no_date_set():
    test_date = "2020-07-25T08:24:19Z"
    config = {"from_date": "",
              "to_date": ""}
    assert date_time_check(test_date, config)
