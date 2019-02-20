GROUP_ID_TO_CONTAINER = {
    'processed': 'data',
    'upload': 'upload',
    'download': 'download'
}


def group_id_to_container_name(group_id):
    return GROUP_ID_TO_CONTAINER[group_id]


def container_name_to_group_id(container_name):
    container_to_group_id = {(v, k) for k, v in GROUP_ID_TO_CONTAINER.items()}
    return container_to_group_id[container_name]


def item_id_and_extension_to_blob_name(item_id, item_extension):
    return str(item_id) + item_extension


def list_of_item_discts_to_dataframe(item_dicts):
    pass


def list_of_item_dicts_to_tsv(item_dicts):
    pass
