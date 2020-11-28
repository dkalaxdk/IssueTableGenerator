import requests
import json
import re
import codecs
import datetime as dt


# When writing markdown, no packages are used, uses Github Flavoured Markdown.
# When writing latex, some packages are used: Long table, caption

def fetch_data(config):
    pull_requests_and_issues = {}
    for repository in config['repositories']:
        page = 1
        count = config['per_page']
        response = requester_functions(config, repository, page)
        current_rep_pull_requests = {}
        current_rep_issues = {}
        print(f"Fetching from: {repository}")
        while count == config['per_page']:
            print(f"    Received {len(response.json())} issues and pull requests")
            if response.ok:
                for output in response.json():
                    # Checks for a valid response from the Github API.

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


def sort_data(config, pullrequests_and_issues):
    temp_pull_requests_and_issues = {}
    for repository in pullrequests_and_issues.items():
        pull_requests = {}
        issues = {}
        for pr in repository[1]['pr'].items():
            update_pr(pr, pull_requests, config)
        for issue in repository[1]['issues'].items():
            update_issue(issue, issues, config)

        temp_pull_requests_and_issues[repository[0]] = {"issues": issues, "pr": pull_requests}
        # Checks for references to issues, therefore this needs to be run after the two loops above
        for pull_request in pull_requests.items():
            references = re.findall(r"/\d+|\.\d+", pull_request[1]['title'])
            references.extend(re.findall(r"aau-giraf/\w+#\d+|#\d+", pull_request[1]['body']))
            # Ensuring each reference is unique
            pull_request[1]['references'] = unique_list_function(references, repository[0])

        temp_pull_requests_and_issues[repository[0]] = {"issues": issues, "pr": pull_requests}

    return temp_pull_requests_and_issues


def contains_correct_labels(config, input_item):
    if len(config['required_labels']) > 0:
        for label in config['required_labels']:
            for output_label in input_item[1]['labels']:
                if label in output_label['name']:
                    return True
        return False
    return True


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
                repository_name = ref[1]
                item_id = int(ref[0])
                if item_id in pr_and_issues[repository_name]['issues']:
                    pr_and_issues[repository_name]['issues'][item_id]['solved_by'][pr[0]] = repository[0]


def update_pr(pr, pull_requests, config):
    if config['state'] == "closed":
        if date_time_check(pr[1]['closed_at'], config):
            if "Revert" not in pr[1]['title'] or "Merge" not in pr[1]['title']:
                write_pr(pr, pull_requests, config)
    else:
        if date_time_check(pr['created_at'], config):
            write_pr(pr, pull_requests, config)


def write_pr(pr, pull_requests, config):
    if pr[0] not in pull_requests:
        pull_requests[pr[0]] = {'title': pr[1]['title'],
                                'body': pr[1]['body']}


def update_issue(issue, issues, config):
    # Checks whether it is a pull request
    if config['state'] == "closed":
        if "Revert" not in issue[1]['title'] or "Merge" not in issue[1]['title']:
            if date_time_check(issue[1]['closed_at'], config):
                write_issue(issue, issues, config)

    else:
        if date_time_check(issue['created_at'], config):
            write_issue(issue, issues, config)


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


def output_generator(pull_requests_and_issues, config):
    output_string = ""
    if config['language'] == "markdown":
        f = codecs.open("output.md", encoding='utf-8', mode='w+')
        for repository in pull_requests_and_issues.items():
            output_string = markdown_format(output_string, repository)
        f.write(output_string)
        f.close()
    if config['language'] == "latex":
        f = codecs.open("output.tex", encoding='utf-8', mode='w+')
        for repository in pull_requests_and_issues.items():
            output_string = latex_format(output_string, repository)
        f.write(output_string)
        f.close()


def markdown_format(output_string, repository):
    output_string += f"# {repository[0]}  \n"
    issues = repository[1]['issues']
    pull_requests = repository[1]['pr']
    # If there are issues, write this:
    if len(issues.items()) > 0:
        output_string += "## Issues  \n"
        output_string += "| Issue NR | Title | Type | Solved By | \n" \
                         "|:---------:|:-----|:-------------|:-------------| \n"
        for issue in issues.items():
            pretty_references = ""
            for reference in issue[1]['solved_by'].items():
                pretty_references += f"[{reference[0]}](https://github.com/aau-giraf/" \
                                     f"{reference[1]}/issues/{reference[0]}) "
            output_string += f"|[{issue[0]}](https://github.com/aau-giraf/{repository[0]}/issues/{issue[0]}) " \
                             f"| {issue[1]['title']} " \
                             f"| {' , '.join(issue[1]['labels'])} " \
                             f"| {pretty_references} | \n"
    # If there are pull requests, write this:
    if len(pull_requests.items()) > 0:
        output_string += "## Pull requests   \n"
        output_string += "| Pull NR | Title | References | \n|:---------:|:-----|:-------------| \n"

        for pull_request in pull_requests.items():
            pretty_references = ""
            for reference in pull_request[1]['references'].items():
                pretty_references += f"[{reference[0]}](https://github.com/aau-giraf/" \
                                     f"{reference[1]}/issues/{reference[0]}) "

            output_string += f"| [{pull_request[0]}](https://github.com/aau-giraf/" \
                             f"{repository[0]}/issues/{pull_request[0]}) " \
                             f"| {pull_request[1]['title']} " \
                             f"| {pretty_references} | \n"
    return output_string


def latex_format(output_string, repository):
    output_string += f"# {repository[0]}  \n"
    issues = repository[1]['issues']
    pull_requests = repository[1]['pr']
    # If there are issues, write this:
    if len(issues.items()) > 0:
        output_string += "\\section{Issues}  \n"
        output_string += '\\begin{longtable}[H]{|l|p{6.3cm}|l|l|} \n' \
                         '\\hline \\endfirsthead ' \
                         '\\textbf{Issues NR} & \\textbf{Title} & \\textbf{Status} & \\textbf{Type} \\\\ ' \
                         '\\hline\n '
        for x in issues.items():
            output_string += f"{repository[0]}\\#{x[0]} & {x[1]['title']} & &  \\\\ \\hline \n"
        output_string += "\\caption{Text} \n\\label{tab:my_tab} \n\\end{longtable} \n \n"
    # If there are pull requests, write this:
    if len(pull_requests.items()) > 0:
        output_string += "\\section{Pull requests}  \n"
        output_string += '\\begin{longtable}[H]{|l|p{6.3cm}|l|l|} \n' \
                         '\\hline \\endfirsthead ' \
                         '\\textbf{Issues NR} & \\textbf{Title} & \\textbf{Status} & \\textbf{Type} \\\\ ' \
                         '\\hline\n'

        for x in pull_requests.items():
            output_string += f"{repository[0]}\\#{x[0]} & {x[1]['title']} & &  \\\\ \\hline \n"
    return output_string


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
