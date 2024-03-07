from plone.restapi.services.types.get import TypesGet
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
from plone.app.uuid.utils import uuidToObject
from uuid import uuid4


@implementer(IPublishTraverse)
class InteraktivTemplatesTypesGet(TypesGet):

    def reply_for_type(self):
        schema = super().reply_for_type()

        if 'blocks_layout' not in schema['properties']:
            return schema

        template_uid = self.request.form.get('template', '')
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
