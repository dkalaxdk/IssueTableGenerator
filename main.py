import requests
from github import Github
import datetime

o_auth_code = "3973464c1860b6ec92b64b87e0b50570c0a14227"
username = "aau-giraf"
url = f"https://api.github.com/repo/{username}"
# pygithub object
g = Github(o_auth_code)
# get that user by username
user = g.get_user(username)
#file = open("output.txt", "w+")
output = ""

date = datetime.datetime(2020, 9, 1, 0, 0)

for repo in user.get_repos():
    if repo.pushed_at.month == datetime.date.today().month:
        print(repo.__str__())

        print("=================================================== \n \n \n")
        print("Issues:")
        print("===================================================")
        for issue in repo.get_issues(state="closed", since=date):
            print("    " + issue.title)
            issue.
        print("=================================================== \n \n \n")
