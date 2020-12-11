class Pr:
    number = 0
    title = ""
    labels = {}
    state = ""
    milestone = ""
    created_at = ""
    closed_at = ""
    body = ""
    references = {}

    def __init__(self, input_issue=None):
        if input_issue is None:
            input_issue = {}
        self.number = input_issue['number']
        self.title = input_issue['title']
        self.labels = input_issue['labels']
        self.state = input_issue['state']
        self.milestone = input_issue['milestone']
        self.closed_at = input_issue['closed_at']
        self.created_at = input_issue['created_at']
        self.body = input_issue['body']
        if input_issue.get('references'):
            self.references = input_issue['references']
        else:
            self.references = {}
