class Item:
    number = 0
    title = ""
    labels = {}
    state = ""
    milestone = ""
    created_at = ""
    closed_at = ""
    body = ""
    is_pull_request = bool

    def return_key(self, key):
        pass

    def __eq__(self, other):
        if isinstance(other, int):
            return self.number == other
        if not isinstance(other, Item):
            # don't attempt to compare against unrelated types
            return False

        return self.number == other.number
