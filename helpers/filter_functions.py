import datetime as dt
from helpers import item_updater as iu
from helpers import reference_manager as rm
from classes.repository import *


def filter_data(config, pull_requests_and_issues):
    temp_pull_requests_and_issues = {}
    for repository in pull_requests_and_issues.items():
        pull_requests = {}
        issues = {}
        for pr in repository[1]['pr'].items():
            iu.update_pr(pr, pull_requests, config)
            rm.pr_reference_to_issues(pr, repository[0])
        for issue in repository[1]['issues'].items():
            iu.update_issue(issue, issues, config)

        current_repository = Repository(repository[0], issues, pull_requests)
        temp_pull_requests_and_issues[current_repository.name] = current_repository

    return temp_pull_requests_and_issues


def issue_checklist(config, issue):
    if config['issues_or_pr'] == "Issues" or config['issues_or_pr'] == "Both":
        if config['state'] == "closed":
            return date_time_check(issue[1]['closed_at'], config) \
                   and not issue_title_contains_blacklisted_word(issue[1], config) \
                   and issue_in_milestone(issue[1], config)

        else:
            return date_time_check(issue[1]['created_at'], config) \
                   and not issue_title_contains_blacklisted_word(issue[1], config) \
                   and issue_in_milestone(issue[1], config)


def pr_checklist(config, pr):
    if config['issues_or_pr'] == "Pull requests" or config['issues_or_pr'] == "Both":
        if config['state'] == "closed":
            return date_time_check(pr[1]['closed_at'], config) \
                   and not pr_title_contains_blacklisted_word(pr[1], config)
        else:
            return date_time_check(pr[1]['created_at'], config) \
                   and not pr_title_contains_blacklisted_word(pr[1], config)


def pr_title_contains_blacklisted_word(item, config):
    if config['blacklist_words_pr']:
        return any(word in item['title'] for word in config['blacklist_words_pr'])
    return False


def issue_title_contains_blacklisted_word(item, config):
    if config['blacklist_words_issue']:
        return any(word in item['title'] for word in config['blacklist_words_issue'])
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
        if issue.get('milestone'):
            return issue['milestone']['title'] == config['milestone']
        else:
            return False
    return True


def contains_correct_labels(config, input_item):
    if config['required_labels']:
        for label in config['required_labels']:
            for output_label in input_item[1]['labels']:
                if label in output_label['name']:
                    return True
        return False
    return True
