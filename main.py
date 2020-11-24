import requests
import json
import re
import codecs
import datetime

data = ""
accept_header = 'application/application/vnd.github.v3+json'
with open("configFile.json", "r") as json_file:
    data = json.load(json_file)

token = data['token']
headers = {'Authorization': 'token ' + token, 'Accept': accept_header}

closed_date = "state=closed"
query = "?" + closed_date
api_root = "https://api.github.com/"
repositories = ["weekplanner", "web-api", "api_client", "wiki"]

all_pr_and_issues = {}
issues = {}

f = codecs.open("output.md", encoding='utf-8', mode='w+')
outputString = ""


for repository in repositories:
    response = requests.get(api_root + "repos/aau-giraf/" + repository + "/issues" + query,
                            headers=headers)
    temp_pull_requests = {}
    temp_issues = {}

    for output in response.json():
        if datetime.datetime.strptime(output['closed_at'], '%Y-%m-%dT%H:%M:%SZ') > datetime.datetime(2020, 9, 1):
            if not output.get('pull_request'):
                if output['number'] not in temp_issues:
                    if "Revert" not in output['title'] or "Merge" not in output['title']:
                        temp_issues[output['number']] = {'title': output['title'], 'body': output['body']}

            if output.get('pull_request'):
                if output['number'] not in temp_pull_requests:
                    if "Revert" not in output['title'] or "Merge" not in output['title']:
                        temp_pull_requests[output['number']] = {'title': output['title'], 'body': output['body']}

    for pull_request in temp_pull_requests.items():
        references = re.findall(r"\d+|\.\d+", pull_request[1]['title'])
        references.extend(re.findall(r"#\d+", pull_request[1]['body']))

        # Ensuring each reference is unique
        unique_list = []
        for x in references:
            if '#' in x:
                x = x[1:]
            if x not in unique_list and '.' not in x:
                unique_list.append(f"[{x}](https://github.com/aau-giraf/{repository}/issues/{x})")
        pull_request[1]['references'] = unique_list

    outputString += f"# {repository}  \n"
    if len(temp_issues.items()) > 0:
        outputString += "## Issues  \n"
        outputString += "| Issue NR | Title | \n|:---------:|:-----| \n"
        for x in temp_issues.items():
            outputString += f"|{x[0]} | {x[1]['title']} |  \n"
    if len(temp_pull_requests.items()) > 0:
        outputString += "## Pull requests   \n"
        outputString += "| Pull NR | Title | References | \n|:---------:|:-----|-------------| \n"

        for x in temp_pull_requests.items():
            outputString += f"| {x[0]} | {x[1]['title']} | {' , '.join(x[1]['references'])}| \n"

f.write(outputString)
f.close()
