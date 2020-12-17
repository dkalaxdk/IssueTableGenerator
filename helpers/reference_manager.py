import re
from classes.config import *


def solved_by_finder(repositories):
    for repository in repositories:
        for pull_request in repository.pull_requests:
            for reference in pull_request.references.items():
                repository_index = return_list_number(repositories, "name", reference[1])
                if repository_index > -1:
                    issue_index = return_list_number(repositories[repository_index].issues, "number", reference[0])
                    if issue_index > -1:
                        repositories[repository_index].issues[issue_index].solved_by[
                            pull_request.number] = repository.name

    return repositories


def return_list_number(input_list, object_property, query):
    for x, item in enumerate(input_list):
        try:
            compare_value = str(item.__getattribute__(object_property))
        except AttributeError:
            return -2
        if compare_value == str(query):
            return x
    return -1


def pr_reference_to_issues(pull_request, repository):
    repository_owner = ConfigManager.fetch('rep_owner')
    # Checks for references to issues, therefore this needs to be run after the two loops above
    references = re.findall(r"/\d+|\.\d+", pull_request.title)
    references.extend(re.findall(rf"{repository_owner}/\w+#\d+|#\d+", pull_request.body))
    # Ensuring each reference is unique
    output = unique_list_to_dictionary(references, repository)
    pull_request.references = output


def clean_reference(input_string, repository):
    repository_owner = ConfigManager.fetch('rep_owner')
    if '#' in input_string[:1] or input_string[:1] == "/":
        # If it is in x then remove it from x
        input_string = input_string[1:]
    if f'{repository_owner}/' in input_string:
        input_string = input_string.split(f"{repository_owner}/")[1]
        split = input_string.split("#")
        repository = split[0]
        input_string = split[1]
    return [input_string, repository]


def unique_list_to_dictionary(references, input_repository):
    unique_list = {}
    repository = input_repository
    for ref in references:
        if ref:
            clean_ref = clean_reference(ref, repository)
            if clean_ref[0] not in unique_list and '.' not in ref:
                if clean_ref[1]:
                    unique_list[clean_ref[0]] = clean_ref[1]
                else:
                    unique_list[clean_ref[0]] = repository
    return unique_list
