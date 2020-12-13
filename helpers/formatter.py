from abc import ABC, abstractmethod


# Abstract base class that provides a common interface
class AbstractFormatter(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def format(self, output_string, repository, config):
        pass


# The concrete classes could and probably should be moved to files of their own
# but I didn't feel like it
class MarkdownFormatter(AbstractFormatter):

    def format(self, output_string, repository, config):
        output_string += f"# {repository.name}  \n"
        issues = repository.issues
        pull_requests = repository.pull_requests
        # If there are issues, write this:
        if len(issues) > 0:
            output_string += "## Issues  \n"
            output_string = markdown_header_creation(output_string, config['issue_headers'])
            output_string = markdown_table_creation(output_string, config['issue_headers'],
                                                    config['issue_table_content'], issues)
            output_string += "\n \n \n"
        if len(pull_requests) > 0:
            output_string += "## Pull requests   \n"
            output_string = markdown_header_creation(output_string, config['pr_headers'])
            output_string = markdown_table_creation(output_string, config['pr_headers'],
                                                    config['pr_table_content'], pull_requests)
            output_string += "\n \n \n"
        return output_string


class LatexFormatter(AbstractFormatter):

    def format(self, output_string, repository, config):
        output_string += f"# {repository.name}  \n"
        issues = repository.issues
        pull_requests = repository.pull_requests
        # If there are issues, write this:
        if len(issues) > 0:
            output_string += "\\section{Issues}  \n"
            output_string = latex_header_creation(output_string, config['issue_headers'])
            output_string = latex_table_creation(output_string, config['issue_headers'], config['issue_table_content'],
                                                 issues)
            output_string += "\\caption{Text} \n\\label{tab:my_tab} \n\\end{longtable} \n \n"
        # If there are pull requests, write this:
        if len(pull_requests) > 0:
            output_string += "\\section{Pull requests}  \n"
            output_string = latex_header_creation(output_string, config['pr_headers'])
            output_string = latex_table_creation(output_string, config['pr_headers'], config['pr_table_content'],
                                                 pull_requests)
            output_string += "\\caption{Text} \n\\label{tab:my_tab} \n\\end{longtable} \n \n"
        return output_string


def latex_header_creation(input_string, headers):
    input_string += '\\begin{longtable}[H]{'
    # Creates appropriate amount of |l| for the table
    for _ in headers:
        input_string += '|l|'
    input_string += '} \n \\hline \\endfirsthead \\\\ '
    # Add the headers defined in the config
    for item in headers:
        input_string += f' \\textbf{{{item}}} &'
    input_string = input_string[:-1]
    input_string += '\\\\ \\hline\n '
    return input_string


def latex_table_creation(input_string, headers, table_content, items):
    # Table content creator:
    extra_table_markers = len(headers) - len(table_content)
    for item in items:
        for content_key in table_content:
            content = item.return_key(key=content_key)
            if isinstance(content, dict):
                if len(content) > 0:
                    for element in content.items():
                        input_string += f"\\href{{https://github.com/aau-giraf/" \
                                        f"{element[1]}/issues/{element[0]}}}{{{element[0]}}}"
                    input_string += "&"
            else:
                input_string += f"{content} &"
        input_string = input_string[:-1]
        for _ in range(extra_table_markers):
            input_string += " & "
        input_string += "\\\\ \\hline \n"
    return input_string


def markdown_header_creation(input_string, headers):
    # Add the headers defined in the config
    input_string += "|"
    for item in headers:
        input_string += f'{item} |'
    input_string += " \n |"
    for _ in headers:
        input_string += ':---------:|'
    input_string += "\n"
    return input_string


def markdown_table_creation(input_string, headers, table_content, items):
    extra_table_markers = len(headers) - len(table_content)
    for item in items:
        for content_key in table_content:
            content = item.return_key(key=content_key)
            if isinstance(content, dict):
                if len(content) > 0:
                    for element in content.items():
                        input_string += f"[{element[0]}](https://github.com/aau-giraf/" \
                                        f"{element[1]}/issues/{element[0]}) "
            else:
                input_string += f"{content} |"
        for _ in range(extra_table_markers):
            input_string += " |"
        input_string += " \n"
    return input_string
