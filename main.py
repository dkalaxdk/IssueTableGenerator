import json
import codecs
from helpers.filter_functions  import *
from helpers.fetcher_functions import *
from helpers.reference_manager import *
from helpers.formatter import MarkdownFormatter, LatexFormatter


# When writing markdown, no packages are used, uses Github Flavoured Markdown.
# When writing latex, some packages are used: Long table, caption


# If the language is not defined correctly this will not work correctly
# But it should not be the responsibility of this class to validate it
def output_generator(repositories, config):
    # This can be generalised to support any format
    # and remove the sequence of 'if' statments
    if config['language'] == "markdown":
        f = codecs.open("output.md", encoding='utf-8', mode='w+')
        formatter = MarkdownFormatter()
    else:
        f = codecs.open("output.tex", encoding='utf-8', mode='w+')
        formatter = LatexFormatter()

    output_string = ""
    for repository in repositories:
        output_string = formatter.format(output_string, repository, config)
    f.write(output_string)
    f.close()


def config_reader():
    with open("configFile.json", "r") as json_file:
        config = json.load(json_file)
    return config


def main(config=None):
    if config is None:
        config = config_reader()
    print("Fetching data...")
    pull_requests_and_issues = fetch_data(config)
    print("Sorting outputs")
    pull_requests_and_issues = filter_data(config, pull_requests_and_issues)

    pull_requests_and_issues = solved_by_finder(pull_requests_and_issues)
    print("Generating file")
    output_generator(pull_requests_and_issues, config)
    print("File generated")
    return True


if __name__ == "__main__":
    main()
