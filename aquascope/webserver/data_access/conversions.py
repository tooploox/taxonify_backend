GROUP_ID_TO_CONTAINER = {
    'processed': 'data',
    'upload': 'upload',
    'download': 'download'
}


def group_id_to_container_name(group_id):
    return GROUP_ID_TO_CONTAINER[group_id]


def container_name_to_group_id(container_name):
    container_to_group_id = dict((v, k) for k, v in GROUP_ID_TO_CONTAINER.items())
    return container_to_group_id[container_name]


def item_to_blob_name(item):
    return str(item._id) + item.extension
