import datetime as dt
from helpers import item_updater as iu
from helpers import reference_manager as rm
from classes.repository import *
from classes.config import *


def filter_data(pull_requests_and_issues):
    temp_pull_requests_and_issues = []
    for repository in pull_requests_and_issues:
        pull_requests = []
        issues = []
        for pr in repository.pull_requests:
            iu.update_pr(pr, pull_requests)
            rm.pr_reference_to_issues(pr, repository.name)
        for issue in repository.issues:
            iu.update_issue(issue, issues)

        temp_pull_requests_and_issues.append(
            Repository(repository.name, issues, pull_requests))

    return temp_pull_requests_and_issues


def issue_checklist(issue):
    if ConfigManager.fetch('state') == "closed":
        compare_date = issue.closed_at
    else:
        compare_date = issue.created_at
    return date_time_check(compare_date) \
           and issue_in_milestone(issue) \
           and contains_correct_labels(issue) \
           and not string_contains_word(issue.title, ConfigManager.fetch('blacklist_words_issue'))


def pr_checklist(pr):
    if ConfigManager.fetch('state') == "closed":
        compare_date = pr.closed_at
    else:
        compare_date = pr.created_at
    return date_time_check(compare_date) \
           and not string_contains_word(pr.title, ConfigManager.fetch('blacklist_words_pr'))


def string_contains_word(title, blacklisted_words):
    if blacklisted_words:
        for word in blacklisted_words:
            if not word == '':
                if word in title:
                    return True
    return False


def date_time_check(input_date):
    to_date = ConfigManager.fetch('to_date')
    from_date = ConfigManager.fetch('from_date')
    format_string = "%Y-%m-%dT%H:%M:%SZ"
    input_format = "%Y-%m-%d"
    closed_at_converted = dt.datetime.strptime(input_date, format_string)
    if from_date and to_date:
        from_date = dt.datetime.strptime(from_date, input_format)
        to_date = dt.datetime.strptime(to_date, input_format)
        return from_date < closed_at_converted < to_date
    if from_date:
        return closed_at_converted > dt.datetime.strptime(
            from_date, input_format)
    if to_date:
        return closed_at_converted < dt.datetime.strptime(
            to_date, input_format)
    else:
        return True


def issue_in_milestone(issue):
    if ConfigManager.fetch('milestone'):
        return issue.milestone == ConfigManager.fetch('milestone')
    else:
        return True


def contains_correct_labels(issue):
    if ConfigManager.fetch('required_labels'):
        for label in ConfigManager.fetch('required_labels'):
            if not label == "":
                for output_label in issue.labels:
                    if label == output_label.name:
                        return True
            else:
                return True
        return False
    return True
