from helpers import filter_functions as ff


def update_pr(pr, pull_requests, config):
    if ff.pr_checklist(config, pr):
        write_pr(pr, pull_requests)


def write_pr(pr, pull_requests):
    if pr[0] not in pull_requests:
        pull_requests[pr[0]] = {'title': pr[1]['title'],
                                'body': pr[1]['body'], 'references': {}}


def update_issue(issue, issues, config):
    if ff.issue_checklist(config, issue):
        write_issue(issue, issues, config)


def write_issue(issue, issues, config):
    if issue[0] not in issues:
        labels = []
        if ff.contains_correct_labels(config, issue):
            for label in issue[1]['labels']:
                if label['name'] in config['type_labels']:
                    labels.append(label['name'])

            issues['labels'] = labels
            issue['solved_by'] = {}
            issues[issue[0]] = issue
