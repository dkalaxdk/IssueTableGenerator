from abc import ABC, abstractmethod
 
# Abstract base class that provides a common interface
class AbstractFormatter(ABC):
 
    def __init__(self):
        self.output_string = output_string
        self.repository = repository
        # 
        super().__init__()
    
    @abstractmethod
    def format(self):
        pass

# The concrete classes could and probably should be moved to files of their own 
# but I didn't feel like it
class MarkdownFormatter(AbstractFormatter):

  def format(self, output_string, repository):
    output_string += f"# {repository[0]}  \n"
    issues = repository[1]['issues']
    pull_requests = repository[1]['pr']
    # If there are issues, write this:
    if len(issues.items()) > 0:
        output_string += "## Issues  \n"
        output_string += "| Issue NR | Title | Labels | Solved By | \n" \
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

class LatexFormatter(AbstractFormatter):

  def format(self, output_string, repository):
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