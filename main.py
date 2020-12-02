import requests
import json
import re
import codecs
import datetime as dt
from formatter import MarkdownFormatter, LatexFormatter


# When writing markdown, no packages are used, uses Github Flavoured Markdown.
# When writing latex, some packages are used: Long table, caption

def fetch_data(config):
    pull_requests_and_issues = {}
    for repository in config['repositories']:
        current_rep_pull_requests = {}
        current_rep_issues = {}

        page = 1
        count = config['per_page']
        response = requester_functions(config, repository, page)
        print(f"Fetching from: {repository}")
        while count != 0:
            print(f"    Received {len(response.json())} issues and pull requests")
            # Checks for a valid response from the Github API.
            if response.ok:
                for output in response.json():
                    if not output.get("pull_request"):
                        current_rep_issues[output['number']] = output
                    else:
                        current_rep_pull_requests[output['number']] = output
                page += 1
                response = requester_functions(config, repository, page)
                count = len(response.json())
            else:
                print("Error receiving content from GitHub")
                print(response.json())
                break

        pull_requests_and_issues[repository] = {"issues": current_rep_issues, "pr": current_rep_pull_requests}
    return pull_requests_and_issues


def requester_functions(config, repository, page):
    query = "?" + "state=" + config['state'] + f"&per_page={config['per_page']}&page={page}"
    accept_header = 'application/vnd.github+json'
    api_root = "https://api.github.com/"
    headers = {'Authorization': 'token ' + config['token'], 'Accept': accept_header}
    return requests.get(api_root + "repos/aau-giraf/" + repository + "/issues" + query,
                        headers=headers)


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


def contains_correct_labels(config, input_item):
    if config['required_labels']:
        for label in config['required_labels']:
            for output_label in input_item[1]['labels']:
                if label in output_label['name']:
                    return True
        return False
    return True


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
    if pr_checklist(config, pr):
        write_pr(pr, pull_requests)


def pr_checklist(config, pr):
    if config['state'] == "closed":
        return date_time_check(pr[1]['closed_at'], config) \
               and not pr_title_contains_blacklisted_word(pr, config)
    else:
        return date_time_check(pr[1]['created_at'], config) \
               and not pr_title_contains_blacklisted_word(pr, config)


def write_pr(pr, pull_requests):
    if pr[0] not in pull_requests:
        pull_requests[pr[0]] = {'title': pr[1]['title'],
                                'body': pr[1]['body'], 'references': {}}


def pr_title_contains_blacklisted_word(item, config):
    if config['blacklist_words_pr']:
        return not any(word in item[1]['title'] for word in config['blacklist_words_pr'])
    return False


def issue_title_contains_blacklisted_word(item, config):
    if config['blacklist_words_issue']:
        return not any(word in item[1]['title'] for word in config['blacklist_words_issue'])
    return False


def update_issue(issue, issues, config):
    if issue_checklist(config, issue):
        write_issue(issue, issues, config)


def issue_checklist(config, issue):
    if config['state'] == "closed":
        return date_time_check(issue[1]['closed_at'], config) \
               and not issue_title_contains_blacklisted_word(issue, config) \
               and issue_in_milestone(issue, config)

    else:
        return date_time_check(issue[1]['created_at'], config) \
               and not issue_title_contains_blacklisted_word(issue, config) \
               and issue_in_milestone(issue, config)


def issue_in_milestone(issue, config):
    if config['milestone']:
        if issue[1].get('milestone'):
            return issue[1]['milestone']['title'] == config['milestone']
        else:
            return False
    return True


def write_issue(issue, issues, config):
    if issue[0] not in issues:
        labels = []
        if contains_correct_labels(config, issue):
            for label in issue[1]['labels']:
                if label['name'] in config['type_labels']:
                    labels.append(label['name'])
            issues[issue[0]] = {'title': issue[1]['title'], 'body': issue[1]['body'],
                                "labels": labels, "solved_by": {}}


def date_time_check(closed_at, config):
    format_string = "%Y-%m-%dT%H:%M:%SZ"
    input_format = "%Y-%m-%d"
    closed_at_converted = dt.datetime.strptime(closed_at, format_string)
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
    pull_requests_and_issues = fetch_data(config)
    print("Sorting outputs")
    pull_requests_and_issues = sort_data(config, pull_requests_and_issues)

    solved_by_finder(pull_requests_and_issues)
    print("Generating file")
    output_generator(pull_requests_and_issues, config)
    print("File generated")


if __name__ == "__main__":
    main()
