class Repository:
    name = ""
    issues = {}
    pull_requests = {}

    def __init__(self, name, issues, pull_requests):
        self.name = name
        self.issues = issues
        self.pull_requests = pull_requests
