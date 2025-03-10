import os
import subprocess
import base64
import secrets
import string

from ZPublisher.HTTPRequest import HTTPRequest
from plone.app.uuid.utils import uuidToObject
from uuid import uuid4
from sqlalchemy.dialects import registry
from zope.component import getUtility
from zope.globalrequest import getRequest
from interaktiv.templates import logger
from typing import Dict
from plone import api

from interaktiv.templates.registry.template import ITemplateSchema



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


def get_thumbnail(template_path) -> bytes:
    path = os.path.dirname(os.path.abspath(__file__))

    try:
        screenshot = subprocess.check_output([
            'node',
            path + "/screencap.js",
            template_path,
            api.portal.get_registry_record(name='thumbnail_user_username', interface=ITemplateSchema),
            api.portal.get_registry_record(name='thumbnail_user_password', interface=ITemplateSchema),
        ], stderr=subprocess.STDOUT)

        return base64.b64decode(screenshot)

    except subprocess.CalledProcessError as e:
        logger.error("Thumbnail creation failed for: %s", str(template_path))
    except Exception as e:
        logger.exception("Unexpected error generating thumbnail for %s: %s", template_path, str(e))


def create_response(
        request: HTTPRequest,
        code: int, msg: str,
        **kwargs
) -> Dict[str, str]:
    request.response.setStatus(code)

    result = {"message": msg}

    if kwargs:
        result.update(kwargs)

    return result

def generate_secure_password(length: int = 16) -> str:
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))