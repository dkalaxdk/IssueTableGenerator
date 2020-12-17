import requests
from classes.issues import *
from classes.pull_requests import *
from classes.repository import *
from classes.config import *


def requester_functions(repository, page):
    query = "?" + "state=" + ConfigManager.fetch(
        'state') + f"&per_page={ConfigManager.fetch('per_page')}&page={page}"
    accept_header = 'application/vnd.github+json'
    api_root = "https://api.github.com/"
    token = ConfigManager.fetch("token")
    rep_owner = ConfigManager.fetch("rep_owner")
    password = ConfigManager.fetch("password")
    if token:
        headers = {'Authorization': 'token ' + token, 'Accept': accept_header}
    else:
        headers = {'u': token + ":" + password, 'Accept': accept_header}
    return requests.get(api_root + "repos/" + rep_owner + "/" + repository + "/issues" + query,
                        headers=headers)


def fetch_data():
    pull_requests_and_issues = []
    for repository in ConfigManager.fetch('repositories'):
        current_rep_pull_requests = []
        current_rep_issues = []

        page = 1
        count = ConfigManager.fetch('per_page')
        response = requester_functions(repository, page)
        print(f"Fetching from: {repository}")
        while count != 0:
            print(f"    Received {len(response.json())} issues and pull requests")
            # Checks for a valid response from the Github API.
            if response.ok:
                for output in response.json():
                    if not output.get("pull_request"):
                        current_rep_issues.append(Issue(output))
                    else:
                        current_rep_pull_requests.append(Pr(output))
                page += 1
                response = requester_functions(repository, page)
                count = len(response.json())
            else:
                print("Error receiving content from GitHub")
                print(repository[0])
                print(response.json())
                break

        pull_requests_and_issues.append(Repository(repository, current_rep_issues, current_rep_pull_requests))
    return pull_requests_and_issues
