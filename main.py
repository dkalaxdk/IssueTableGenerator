import requests
import json
import re
import codecs
import datetime as dt


# When writing markdown, no packages are used, uses Github Flavoured Markdown.
# When writing latex, some packages are used: Longtable, caption

def api_fetcher_and_sorter(data):
    query = "?state=closed"
    accept_header = 'application/vnd.github+json'
    repositories = data['repositories']
    api_root = "https://api.github.com/"
    headers = {'Authorization': 'token ' + data['token'], 'Accept': accept_header}
    pull_requests_and_issues = {}
    for repository in repositories:
        response = requests.get(api_root + "repos/aau-giraf/" + repository + "/issues" + query,
                                headers=headers)
        temp_pull_requests = {}
        temp_issues = {}
        for output in response.json():
            # Checks for a valid response from the Github API.
            if response.ok:
                if date_time_check(output['closed_at'], data):
                    if "Revert" not in output['title'] or "Merge" not in output['title']:
                        if not output.get('pull_request'):
                            if output['number'] not in temp_issues:
                                temp_issues[output['number']] = {'title': output['title'], 'body': output['body'],
                                                                 "references": []}

                        if output.get('pull_request'):
                            if output['number'] not in temp_pull_requests:
                                temp_pull_requests[output['number']] = {'title': output['title'],
                                                                        'body': output['body']}

                for pull_request in temp_pull_requests.items():
                    references = re.findall(r"\d+|\.\d+", pull_request[1]['title'])
                    references.extend(re.findall(r"#\d+", pull_request[1]['body']))
                    # Ensuring each reference is unique
                    pull_request[1]['references'] = unique_list_function(references, repository)

            else:
                print("Error receiving content from GitHub")
                print(response.json())
                break
        pull_requests_and_issues[repository] = {"issues": temp_issues, "pr": temp_pull_requests}
    return pull_requests_and_issues


def unique_list_function(references, repository):
    unique_list = []
    for x in references:
        if '#' in x:
            x = x[1:]
        if x not in unique_list and '.' not in x:
            unique_list.append(f"[{x}](https://github.com/aau-giraf/{repository}/issues/{x})")
    return unique_list


def date_time_check(closed_at, data):
    format_string = "%Y-%m-%dT%H:%M:%SZ"
    input_format = "%Y-%m-%d"
    closed_at_converted = dt.datetime.strptime(closed_at, format_string)
    if len(data['closed_after']) > 0 and len(data['closed_before']) > 0:
        closed_after = dt.datetime.strptime(data['closed_after'], input_format)
        closed_before = dt.datetime.strptime(data['closed_before'], input_format)
        return closed_at_converted > closed_after and closed_at_converted < closed_before
    if len(data['closed_after']) > 0:
        return closed_at_converted > dt.datetime.strptime(
            data['closed_after'], input_format)
    if len(data['closed_after']) > 0:
        return closed_at_converted < dt.datetime.strptime(
            data['closed_before'], input_format)


def output_generator(pull_requests_and_issues, data):
    output_string = ""
    f = codecs.open("output.txt", encoding='utf-8', mode='w+')
    if data['language'] == "markdown":
        for repository in pull_requests_and_issues.items():
            output_string = markdown_format(output_string, repository)
    if data['language'] == "latex":
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
        output_string += "| Issue NR | Title | Fixed By | \n|:---------:|:-----|:-------------| \n"
        for x in issues.items():
            output_string += f"|{x[0]} | {x[1]['title']} | {' , '.join(x[1]['references'])}| \n"
    # If there are pull requests, write this:
    if len(pull_requests.items()) > 0:
        output_string += "## Pull requests   \n"
        output_string += "| Pull NR | Title | References | \n|:---------:|:-----|:-------------| \n"

        for x in pull_requests.items():
            output_string += f"| {x[0]} | {x[1]['title']} | {' , '.join(x[1]['references'])}| \n"
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
        data = json.load(json_file)
    return data


def main():
    data = config_reader()
    pull_requests_and_issues = api_fetcher_and_sorter(data)
    output_generator(pull_requests_and_issues, data)


if __name__ == "__main__":
    main()
