from classes.pull_requests import Pr
from helpers.item_updater import *
from classes.issues import Issue


def test_write_pr_written():
    test_number = 5
    pr = Pr()
    pr.number = test_number
    pull_requests = []
    first_len = len(pull_requests)
    write_pr(pr, pull_requests)
    second_len = len(pull_requests)
    assert first_len < second_len


def test_write_pr_written_false_already_in_list():
    test_number = 5
    pr = Pr()
    pr.number = test_number
    pull_requests = [pr]
    first_len = len(pull_requests)
    write_pr(pr, pull_requests)
    second_len = len(pull_requests)
    assert first_len == second_len


def test_write_issue_written():
    test_number = 5
    issue = Issue()
    issue.number = test_number
    issues = []
    first_len = len(issues)
    write_pr(issue, issues)
    second_len = len(issues)
    assert first_len < second_len


def test_write_issue_written_false_already_in_list():
    test_number = 5
    issue = Issue()
    issue.number = test_number
    issues = [issue]
    first_len = len(issues)
    write_pr(issue, issues)
    second_len = len(issues)
    assert first_len == second_len
