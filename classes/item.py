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
        return getattr(self, key, f"{key} is not supported")
