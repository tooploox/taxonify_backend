strings_to_remove = ["Sp", "Sp."]


def add(node, values):
    """Add values as consecutive levels to the node dictionary
    node -- a dictionary
    values -- a list of string values
    """
    if values:
        value = values[0]
        if isinstance(value, str):
            capitalized_value = value.capitalize().strip()
            if capitalized_value not in strings_to_remove:
                if capitalized_value not in node:
                    node[capitalized_value] = {}
                rest = values[1:]
                if rest:
                    add(node[capitalized_value], rest)
