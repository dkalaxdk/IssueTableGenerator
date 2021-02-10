# GirafReleaseDesigner
This python script will generate a markdown table, containing the issues and pull requests, closed in a given time period within Giraf. <br>
It will also add a relation between issues and pull requests, if the naming convention from the project is used. <br>
1. Copy the configFile-template.json to file named configFile.json
2. Update the values to match your criteria.

The script can either be used, by inserting a GitHub username and password, or by using a developer token.

## Config
The script comes equipped with a basic UI, which configures the config file, based on the input. <br>
1. Token: The token is the developer token from github.
2. Username: Github Username
3. Password: Github Password
4. Repository Owner: The owner of the Github Repository
5. Repositories: A Comma separated list of the repositories to look through.
6. From date: A date (year-month-day) used to define when the item should have been created. (Will exclude any items created before this date)
7. To date: Same as above, just to date.
8. Updated after: Same as above, just when it was last updated.
9. Updated before: Same as above, only included items which was updated before this date.
10. State: The state of the items (open, closed, all)
11. Language: Latex or Markdown, defines the output language
12. Results per page: This won't change the output, but may slightly lower the ram usage.
13. Required labels: These labels are required to be on the issues, before it is added to the output. (Comma separated list)
14. Type labels: A comma separated list which will be used in case the Table content of issues is includes to "type"
15. Word blacklist: A comma separated list of items which cannot be a part of the title.
16. A comma separated list of milestones in which the items should be in.
17. Headers: These are the headers which will be used on the table. (Comma separated list)
18. Table content: These are the items which will be inserted into the table.(Comma separated list)
    * On both pull requests and issues these can be:number, title, labels, state, milestone,closed_at.
    * On issues these also can be: created_at,updated_at,body,solved_by.
    * On pull requests, these also can be: references.
19. Issue/Pr filter: This defines whether the output should contain Issues, Pull requests or Both.

