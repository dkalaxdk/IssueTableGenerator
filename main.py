import requests

token = "3973464c1860b6ec92b64b87e0b50570c0a14227"
username = "dkalaxdk"
headers = {'Authorization': 'token ' + token}

closed_date = "closed:>2020-09-01"
query = "??" + closed_date
api_root = "https://api.github.com/"
request_header = {'Accept': 'application/vnd.github.v3+json'}
repositories = ["weekplanner", "web-api", "api_client", "wiki"]

all_pr_and_issues = {}
issues = {}

for repository in repositories:
    response = requests.get(api_root + "repos/aau-giraf/" + repository + "/issues" + query,
                            headers=headers)
    temp_pull_requests = []
    temp_issues = {}

    for output in response.json():
        if not output.get('pull_request'):
            temp_issues[output('number')] = {"title": output['title'], "body": output['body']}

    for output in response.json():
        if output.get('pull_request'):
            temp_pull_requests.append(output['title'])

    pr_and_issues = {"issues": temp_issues, "pr": temp_pull_requests}
    all_pr_and_issues[repository] = pr_and_issues
