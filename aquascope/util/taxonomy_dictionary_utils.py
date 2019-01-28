def add(node, values):
    """Add values as consecutive levels to the node dictionary
    node -- a dictionary
    values -- a list of string values
    """
    if values:
        value = values[0]
        if value not in node:
            node[value] = {}
        rest = values[1:]
        if rest:
            add(node[value], rest)
