class Label:
    name = ""

    def __init__(self, label=None):
        if label is None:
            pass
        else:
            self.name = label['name']
