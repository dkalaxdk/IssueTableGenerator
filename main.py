import requests
import json
import re
import codecs
import datetime as dt
from formatter import MarkdownFormatter, LatexFormatter


# When writing markdown, no packages are used, uses Github Flavoured Markdown.
# When writing latex, some packages are used: Longtable, caption

def result_fetcher_and_sorter(config):
    pull_requests_and_issues = {}
    for repository in config['repositories']:
        page = 1
        count = config['per_page']
        response = requester_functions(config, repository, page)
        current_rep_pull_requests = {}
        current_rep_issues = {}
        print(f"Fetching from: {repository}")
        while count == config['per_page']:
            print(f"Received {len(response.json())} issues")
            for output in response.json():
                # Checks for a valid response from the Github API.
                if response.ok:
                    sort_data(config, output, current_rep_issues, current_rep_pull_requests, repository)
                else:
                    print("Error receiving content from GitHub")
                    print(response.json())
                    break
            page += 1
            response = requester_functions(config, repository, page)
            count = len(response.json())

        pull_requests_and_issues[repository] = {"issues": current_rep_issues, "pr": current_rep_pull_requests}
    return pull_requests_and_issues


def sort_data(config, output, current_rep_issues, current_rep_pull_requests, repository):
    if config['state'] == "closed":
        if date_time_check(output['closed_at'], config):
            if "Revert" not in output['title'] or "Merge" not in output['title']:
                if len(config['labels']) > 0:
                    contains_correct_labels(config, output, current_rep_issues,
                                            current_rep_pull_requests)
                else:
                    update_pr_or_issue(output, current_rep_issues, current_rep_pull_requests)
    if config['state'] != "closed":
        if date_time_check(output['created_at'], config):
            if len(config['labels']) > 0:
                contains_correct_labels(config, output, current_rep_issues, current_rep_pull_requests)
            else:
                update_pr_or_issue(output, current_rep_issues, current_rep_pull_requests)

    for pull_request in current_rep_pull_requests.items():
        references = re.findall(r"/\d+|\.\d+", pull_request[1]['title'])
        references.extend(re.findall(r"aau-giraf/\w+#\d+|#\d+", pull_request[1]['body']))
        # Ensuring each reference is unique
        pull_request[1]['references'] = unique_list_function(references, repository)


def contains_correct_labels(config, output, current_rep_issues, current_rep_pull_requests):
    for label in config['labels']:
        for output_label in output['labels']:
            if label in output_label['name']:
                update_pr_or_issue(output, current_rep_issues, current_rep_pull_requests)


def requester_functions(config, repository, page):
    query = "?" + "state=" + config['state'] + f"&per_page={config['per_page']}&page={page}"
    accept_header = 'application/vnd.github+json'
    api_root = "https://api.github.com/"
    headers = {'Authorization': 'token ' + config['token'], 'Accept': accept_header}
    return requests.get(api_root + "repos/aau-giraf/" + repository + "/issues" + query,
                        headers=headers)


def unique_list_function(references, input_repository):
    unique_list = {}
    repository = input_repository
    for ref in references:
        if len(ref) > 0:
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
                if int(ref[0]) in pr_and_issues[ref[1]]['issues']:
                    pr_and_issues[ref[1]]['issues'][int(ref[0])]['solved_by'][pr[0]] = repository[0]


def update_pr_or_issue(output, issues, pull_requests):
    # Checks whether it is a pull request
    if not output.get('pull_request'):
        if output['number'] not in issues:
            labels = []
            for label in output['labels']:
                if label['name'] == "type: bug" or label['name'] == "type: feature":
                    labels.append(label['name'])
            issues[output['number']] = {'title': output['title'], 'body': output['body'],
                                        "labels": labels, "solved_by": {}}

    if output.get('pull_request'):
        if output['number'] not in pull_requests:
            pull_requests[output['number']] = {'title': output['title'],
                                               'body': output['body']}


def date_time_check(closed_at, config):
    format_string = "%Y-%m-%dT%H:%M:%SZ"
    input_format = "%Y-%m-%d"
    closed_at_converted = dt.datetime.strptime(closed_at, format_string)
    if len(config['from_date']) > 0 and len(config['to_date']) > 0:
        from_date = dt.datetime.strptime(config['from_date'], input_format)
        to_date = dt.datetime.strptime(config['to_date'], input_format)
        return from_date < closed_at_converted < to_date
    if len(config['from_date']) > 0:
        return closed_at_converted > dt.datetime.strptime(
            config['from_date'], input_format)
    if len(config['to_date']) > 0:
        return closed_at_converted < dt.datetime.strptime(
            config['to_date'], input_format)
    else:
        return True


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
    pull_requests_and_issues = result_fetcher_and_sorter(config)
    print("Sorting outputs")
    solved_by_finder(pull_requests_and_issues)
    print("Generating file")
    output_generator(pull_requests_and_issues, config)
    print("File generated")


if __name__ == "__main__":
    main()
