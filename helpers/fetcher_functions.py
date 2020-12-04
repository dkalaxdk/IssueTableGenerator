import requests


def requester_functions(config, repository, page):
    query = "?" + "state=" + config['state'] + f"&per_page={config['per_page']}&page={page}"
    accept_header = 'application/vnd.github+json'
    api_root = "https://api.github.com/"
    if config['token']:
        headers = {'Authorization': 'token ' + config['token'], 'Accept': accept_header}
    else:
        headers = {'u': config['token'] + ":" + config['password'], 'Accept': accept_header}
    return requests.get(api_root + "repos/" + config['rep_owner'] + "/" + repository + "/issues" + query,
                        headers=headers)


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


