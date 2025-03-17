import plone.protect.interfaces

from typing import Dict, NoReturn
from plone.dexterity.content import DexterityContent
from plone.restapi.services import Service
from plone import api
from plone.restapi.deserializer import json_body
from zope.interface import alsoProvides
from plone.namedfile.file import NamedBlobImage
from urllib.parse import urlparse

from interaktiv.templates.utilities.helper import get_thumbnail, create_response
from interaktiv.templates import logger


class TemplateThumbnailPost(Service):

    def reply(self) -> Dict[str, str]:
        if "IDisableCSRFProtection" in dir(plone.protect.interfaces):
            alsoProvides(self.request, plone.protect.interfaces.IDisableCSRFProtection)

        data: Dict = json_body(self.request)

        template = api.content.get(path=data.get("url"))
        if not template:
            return create_response(self.request, 404, "Template not found")

        try:
            if data.get("modified"):
                self._replace_thumbnail(template)
            else:
                self._create_and_assign_template_thumbnail(template)

            return create_response(self.request, 200, "Template thumbnail created successfully")

        except Exception as e:
            return create_response(self.request, 500, "An error occurred while processing the template thumbnail.")
            logger.exception("Error proccesing template thumbnail: %s", str(e))

    def _replace_thumbnail(self, template: DexterityContent) -> NoReturn:
        try:
            if hasattr(template, "template_thumbnail"):
                thumbnail = api.content.get(path=urlparse(template.template_thumbnail).path)

                if thumbnail:
                    thumbnail.image = self._get_thumbnail_image(template.absolute_url())
                    thumbnail.reindexObject(idxs=["image"])

        except Exception as e:
            logger.exception("Error replacing template thumbnail: %s", str(e))
            raise

    def _create_and_assign_template_thumbnail(self, template: DexterityContent) -> NoReturn:
        try:
            thumbnail = api.content.create(
                container=template,
                type='Image',
                title="Template Thumbnail",
                id="template-thumbnail",
                image=self._get_thumbnail_image(template.absolute_url())
            )

            template.template_thumbnail = thumbnail.absolute_url()
            template.reindexObject(idxs=["template_thumbnail"])

        except Exception as e:
            logger.exception("Error creating or assigning template thumbnail: %s", str(e))
            raise

    @staticmethod
    def _get_thumbnail_image(template_url: str) -> NamedBlobImage:
        return NamedBlobImage(data=get_thumbnail(template_url), contentType="image/jpeg", filename="Template Thumbnail")
