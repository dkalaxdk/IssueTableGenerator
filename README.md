# GirafReleaseDesigner
This python script will generate a markdown table, containing the issues and pull requests, closed in a given time period within Giraf. <br>
It will also add a relation between issues and pull requests, if the naming convention from the project is used. <br>
1. Copy the configFile-template.json to file named configFile.json
2. Update the values to match your criteria.

To use this script, a developer code needs to be made through [GitHub](https://github.com/settings/tokens), and placed in the config file.
Within the config file, a start and end date can also be defined, as well as the repositories that should be scanned.

## Config
The config file contains 8 different configurations:
1. Token: This is the token you should generate from [GitHub](https://github.com/settings/tokens).
2. Repositories: This is a list of the repositories that should be included in the search, i.e: ["weekplanner", "web-api", "api_client", "wiki"], would search the mentioned repositories.
3. From_date: This is the date on which to start the search i.e "2020-09-01" would include all issues and pull requests made after "2020-09-01".
4. To_date: Rather obvious, init?
5. State: This is the state of the issue, github allows for either: open,closed or all.
6. Language: The output language of the table, this can either be markdown or latex.
