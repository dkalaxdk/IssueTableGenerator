from helpers import filter_functions as ff
from classes.config import *


def update_pr(pr, pull_requests):
    if ff.pr_checklist(pr):
        write_pr(pr, pull_requests)


def write_pr(pr, pull_requests):
    if pr not in pull_requests:
        pull_requests.append(pr)


def update_issue(issue, issues):
    if ff.issue_checklist(issue):
        write_issue(issue, issues)


def write_issue(issue, issues):
    if not (issue in issues):
        labels = []
        for label in issue.labels:
            if label.name in ConfigManager.fetch('type_labels'):
                labels.append(label.name)

        issue.highlighted_labels = labels
        issues.append(issue)
