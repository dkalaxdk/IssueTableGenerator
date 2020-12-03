import json
import re
import codecs
import filter_functions as ff
import fetcher_functions as fetcher
from formatter import MarkdownFormatter, LatexFormatter


# When writing markdown, no packages are used, uses Github Flavoured Markdown.
# When writing latex, some packages are used: Long table, caption


def sort_data(config, pullrequests_and_issues):
    temp_pull_requests_and_issues = {}
    for repository in pullrequests_and_issues.items():
        pull_requests = {}
        issues = {}
        for pr in repository[1]['pr'].items():
            update_pr(pr, pull_requests, config)
            pr_reference_to_issues(pr, repository[0])
        for issue in repository[1]['issues'].items():
            update_issue(issue, issues, config)

        temp_pull_requests_and_issues[repository[0]] = {"issues": issues, "pr": pull_requests}

    return temp_pull_requests_and_issues


def pr_reference_to_issues(pull_request, repository):
    # Checks for references to issues, therefore this needs to be run after the two loops above
    references = re.findall(r"/\d+|\.\d+", pull_request[1]['title'])
    references.extend(re.findall(r"aau-giraf/\w+#\d+|#\d+", pull_request[1]['body']))
    # Ensuring each reference is unique
    pull_request[1]['references'] = unique_list_function(references, repository)


def unique_list_function(references, input_repository):
    unique_list = {}
    repository = input_repository
    for ref in references:
        if ref:
            clean_ref = clean_reference(ref, repository)
            if clean_ref[0] not in unique_list and '.' not in ref:
                unique_list[clean_ref[0]] = repository
    return unique_list


def clean_reference(input_string, repository):
    if '#' in input_string[:1] or input_string[:1] == "/":
        # If it is in x then remove it from x
        input_string = input_string[1:]
    if 'aau-giraf/' in input_string:
        input_string = input_string.split("aau-giraf/")[1]
        split = input_string.split("#")
        repository = split[0]
        input_string = split[1]
    return [input_string, repository]


def solved_by_finder(pr_and_issues):
    for repository in pr_and_issues.items():
        for pr in repository[1]['pr'].items():
            for ref in pr[1]['references'].items():
                repository_name = ref[1]
                item_id = int(ref[0])
                if item_id in pr_and_issues[repository_name]['issues']:
                    pr_and_issues[repository_name]['issues'][item_id]['solved_by'][pr[0]] = repository[0]


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
            issues[issue[0]] = {'title': issue[1]['title'], 'body': issue[1]['body'],
                                "labels": labels, "solved_by": {}}


# If the language is not defined correctly this will not work correctly
# But it should not be the responsibility of this class to validate it
def output_generator(pull_requests_and_issues, config):
    # This can be generalised to support any format
    # and remove the sequence of 'if' statments
    if config['language'] == "markdown":
        formatter = MarkdownFormatter()
    if config['language'] == "latex":
        formatter = LatexFormatter()

    output_string = ""
    f = codecs.open("output.md", encoding='utf-8', mode='w+')
    for repository in pull_requests_and_issues.items():
        output_string = formatter.format(output_string, repository)
    f.write(output_string)
    f.close()


def config_reader():
    with open("configFile.json", "r") as json_file:
        config = json.load(json_file)
    return config


def main():
    config = config_reader()
    print("Fetching data...")
    pull_requests_and_issues = fetcher.fetch_data(config)
    print("Sorting outputs")
    pull_requests_and_issues = sort_data(config, pull_requests_and_issues)

    solved_by_finder(pull_requests_and_issues)
    print("Generating file")
    output_generator(pull_requests_and_issues, config)
    print("File generated")
    return True


if __name__ == "__main__":
    main()
