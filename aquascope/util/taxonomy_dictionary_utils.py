strings_to_replace_with_not_specified = ["Sp", "Sp."]
not_specified_string = "Not specified"


def add(node, values):
    """Add values as consecutive levels to the node dictionary
    node -- a dictionary
    values -- a list of string values
    """
    if values:
        value = values[0]
        if isinstance(value, str):
            capitalized_value = value.capitalize().strip()
            if capitalized_value in strings_to_replace_with_not_specified:
                capitalized_value = not_specified_string
            if capitalized_value not in node:
                node[capitalized_value] = {}
            rest = values[1:]
            if rest:
                add(node[capitalized_value], rest)
