from classes.item import *


class Pr(Item):

    def __init__(self, input_issue=None):
        if input_issue is None:
            pass
        else:
            self.is_pull_request = True
            self.number = input_issue['number']
            self.title = input_issue['title']
            self.labels = input_issue['labels']
            self.state = input_issue['state']
            self.milestone = input_issue['milestone']
            self.closed_at = input_issue['closed_at']
            self.created_at = input_issue['created_at']
            self.body = input_issue['body']
            self.references = {}

    def return_key(self, key):
        return getattr(self, key, f"{key} is not supported on pull requests")
