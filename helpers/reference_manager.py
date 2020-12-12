import re


def solved_by_finder(pr_and_issues):
    for repository in pr_and_issues:
        for pull_request in repository.pull_requests:
            for reference in pull_request.references.items():
                repo_to_update = next((repo for repo in pr_and_issues if repo.name == reference[1]), None)
                if repo_to_update:
                    issue_to_update = next(
                        (issue for issue in repo_to_update.issues if issue.number == int(reference[0])),
                        None)
                    if issue_to_update:
                        issue_to_update.solved_by[pull_request.number] = reference[1]


def pr_reference_to_issues(pull_request, repository):
    # Checks for references to issues, therefore this needs to be run after the two loops above
    references = re.findall(r"/\d+|\.\d+", pull_request.title)
    references.extend(re.findall(r"aau-giraf/\w+#\d+|#\d+", pull_request.body))
    # Ensuring each reference is unique
    output = unique_list_function(references, repository)
    pull_request.references = output


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


def unique_list_function(references, input_repository):
    unique_list = {}
    repository = input_repository
    for ref in references:
        if ref:
            clean_ref = clean_reference(ref, repository)
            if clean_ref[0] not in unique_list and '.' not in ref:
                unique_list[clean_ref[0]] = repository
    return unique_list
