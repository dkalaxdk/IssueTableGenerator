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
            output_string += "| Issue NR | Title | Labels | Solved By | \n" \
                             "|:---------:|:-----|:-------------|:-------------| \n"
            for issue in issues:
                pretty_references = ""
                for reference in issue[1]['solved_by'].items():
                    pretty_references += f"[{reference[0]}](https://github.com/aau-giraf/" \
                                         f"{reference[1]}/issues/{reference[0]}) "
                output_string += f"|[{issue.number}](https://github.com/aau-giraf/{repository.name}/issues/{issue.number}) " \
                                 f"| {issue.title} " \
                                 f"| {' , '.join(issue.labels)} " \
                                 f"| {pretty_references} | \n"
        # If there are pull requests, write this:
        if len(pull_requests) > 0:
            output_string += "## Pull requests   \n"
            output_string += "| Pull NR | Title | References | \n|:---------:|:-----|:-------------| \n"

            for pull_request in pull_requests:
                pretty_references = ""
                for reference in pull_request.references:
                    pretty_references += f"[{reference[0]}](https://github.com/aau-giraf/" \
                                         f"{reference[1]}/issues/{reference[0]}) "

                output_string += f"| [{pull_request.number}](https://github.com/aau-giraf/" \
                                 f"{repository.name}/issues/{pull_request.number}) " \
                                 f"| {pull_request.title} " \
                                 f"| {pretty_references} | \n"
        return output_string


class LatexFormatter(AbstractFormatter):

    def format(self, output_string, repository, config):
        output_string += f"# {repository.name}  \n"
        issues = repository.issues
        pull_requests = repository.pull_requests
        # If there are issues, write this:
        if len(issues) > 0:
            output_string += "\\section{Issues}  \n"
            output_string += '\\begin{longtable}[H]{'
            for _ in config['headers']:
                output_string += '|l|'
            output_string += '} \n \\hline \\endfirsthead \\\\ '
            for item in config['headers']:
                output_string += f' \\textbf{{ {item}}} &'
            output_string = output_string[:-1]
            output_string += '\\\\ \\hline\n '
            for issue in issues:
                output_string += f"{repository.name}\\#{issue.number} & {issue.title} & &  \\\\ \\hline \n"
            output_string += "\\caption{Text} \n\\label{tab:my_tab} \n\\end{longtable} \n \n"

        # If there are pull requests, write this:
        if len(pull_requests) > 0:
            output_string += "\\section{Pull requests}  \n"
            output_string += '\\begin{longtable}[H]{'
            # Header creation

            # Creates appropriate amount of |l| for the table
            for _ in config['pr_headers']:
                output_string += '|l|'
            output_string += '} \n \\hline \\endfirsthead \\\\ '
            # Add the headers defined in the config
            for item in config['pr_headers']:
                output_string += f' \\textbf{{ {item}}} &'
            output_string = output_string[:-1]
            output_string += '\\\\ \\hline\n '

            # Table content creator:
            extra_table_markers = len(config['pr_headers']) - len(config['pr_table_content'])
            for pull_request in pull_requests:
                for content_key in config['pr_table_content']:
                    output_string += f"{pull_request.return_key(key=content_key)} &"
                output_string = output_string[:-1]
                for _ in range(extra_table_markers):
                    output_string += " & "
                output_string += "\\\\ \\hline \n"
        return output_string
