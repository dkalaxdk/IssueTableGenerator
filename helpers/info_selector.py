def return_key(input_item, key):
    if key == "solved_by":
        if not input_item.get("pull_request"):
            return input_item['solved_by']
        else:
            return "solved_by not supported on pull issues"
    if key == "references":
        if input_item.get("pull_request"):
            return input_item['references']
        else:
            return "references not supported on pull requests"
    elif key == "":
        return ""
    else:
        return input_item[key]
