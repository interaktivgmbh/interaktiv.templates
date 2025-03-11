from plone.app.uuid.utils import uuidToObject
from uuid import uuid4
from zope.globalrequest import getRequest
from typing import Tuple

def get_schema_from_template(schema: dict) -> dict:
    request = getRequest()
    if not request:
        return schema

    if 'blocks_layout' not in schema['properties']:
        return schema

    template_uid = request.form.get('template', '')
    template = uuidToObject(template_uid)

    if not template:
        return schema

    template_blocks = getattr(template, 'blocks', {})
    template_blocks_layout = getattr(template, 'blocks_layout', {})
    if not (template_blocks and template_blocks_layout):
        return schema

    schema['properties']['blocks']['default'] = {}
    schema['properties']['blocks_layout']['default']['items'] = []
    for block_id in template_blocks_layout['items']:
        new_block_id = str(uuid4())

        schema['properties']['blocks']['default'][new_block_id] = template_blocks[block_id]
        schema['properties']['blocks_layout']['default']['items'].append(new_block_id)

    return schema

def common_prefix_length(path1: Tuple[str, ...], path2: Tuple[str, ...]) -> int:
    """
    Calculates the length of the common path prefix of two path tuples.
    """
    count = 0
    for a, b in zip(path1, path2):
        if a == b:
            count += 1
        else:
            break
    return count