from classes.item import *
from classes.label import *


def get_labels(labels):
    output_labels = []
    for label in labels:
        output_labels.append(Label(label))
    return output_labels


class Issue(Item):

    def __init__(self, input_issue=None):
        if input_issue is None:
            pass
        else:
            self.is_pull_request = False
            self.number = input_issue['number']
            self.title = input_issue['title']
            self.labels = get_labels(input_issue['labels'])
            self.state = input_issue['state']
            if input_issue.get('milestone'):
                self.milestone = input_issue['milestone']['title']
            else:
                self.milestone = ""
            self.closed_at = input_issue['closed_at']
            self.created_at = input_issue['created_at']
            self.updated_at = input_issue['updated_at']
            self.body = input_issue['body']
            self.highlighted_labels = []
            self.solved_by = {}

    def return_key(self, key):
        if key == "":
            return ""
        return getattr(self, key, f"{key} is not supported on issues")
