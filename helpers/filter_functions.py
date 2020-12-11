import datetime as dt
from helpers import item_updater as iu
from helpers import reference_manager as rm
from classes.repository import *


def filter_data(config, pull_requests_and_issues):
    temp_pull_requests_and_issues = {}
    for repository in pull_requests_and_issues:
        pull_requests = {}
        issues = {}
        for pr in repository.pull_requests:
            iu.update_pr(pr, pull_requests, config)
            rm.pr_reference_to_issues(pr, repository.name)
        for issue in repository.issues:
            iu.update_issue(issue, issues, config)

        current_repository = Repository(repository.name, issues, pull_requests)
        temp_pull_requests_and_issues[current_repository.name] = current_repository

    return temp_pull_requests_and_issues


def issue_checklist(config, issue):
    if config['issues_or_pr'] == "Issues" or config['issues_or_pr'] == "Both":
        if config['state'] == "closed":
            return date_time_check(issue.closed_at, config) \
                   and not string_contains_word(issue.title, config['blacklist_words_issue']) \
                   and issue_in_milestone(issue, config)

        else:
            return date_time_check(issue.created_at, config) \
                   and not string_contains_word(issue.title, config['blacklist_words_issue']) \
                   and issue_in_milestone(issue, config)


def pr_checklist(config, pr):
    if config['issues_or_pr'] == "Pull requests" or config['issues_or_pr'] == "Both":
        if config['state'] == "closed":
            return date_time_check(pr.closed_at, config) \
                   and not string_contains_word(pr.title, config['blacklist_words_pr'])
        else:
            return date_time_check(pr.created_at, config) \
                   and not string_contains_word(pr.title, config['blacklist_words_pr'])


def string_contains_word(title, blacklisted_words):
    if blacklisted_words:
        return any(word in title for word in blacklisted_words)
    return False


def date_time_check(input_date, config):
    format_string = "%Y-%m-%dT%H:%M:%SZ"
    input_format = "%Y-%m-%d"
    closed_at_converted = dt.datetime.strptime(input_date, format_string)
    if config['from_date'] and config['to_date']:
        from_date = dt.datetime.strptime(config['from_date'], input_format)
        to_date = dt.datetime.strptime(config['to_date'], input_format)
        return from_date < closed_at_converted < to_date
    if config['from_date']:
        return closed_at_converted > dt.datetime.strptime(
            config['from_date'], input_format)
    if config['to_date']:
        return closed_at_converted < dt.datetime.strptime(
            config['to_date'], input_format)
    else:
        return True


def issue_in_milestone(issue, config):
    if config['milestone']:
        return issue.milestone == config['milestone']
    else:
        return False


def contains_correct_labels(config, issue):
    if config['required_labels']:
        for label in config['required_labels']:
            for output_label in issue.labels:
                if label == output_label.name:
                    return True
        return False
    return True
