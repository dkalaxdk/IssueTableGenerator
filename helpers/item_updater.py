from helpers import filter_functions as ff


def update_pr(pr, pull_requests, config):
    if ff.pr_checklist(config, pr):
        write_pr(pr, pull_requests)


def write_pr(pr, pull_requests):
    if pr not in pull_requests:
        pull_requests.append(pr)


def update_issue(issue, issues, config):
    if ff.issue_checklist(config, issue):
        write_issue(issue, issues, config)


def write_issue(issue, issues, config):
    if issue not in issues:
        labels = []
        for label in issue.labels:
            if label['name'] in config['type_labels']:
                labels.append(label['name'])

        issue.highlighted_labels = labels
        issues.append(issues)
