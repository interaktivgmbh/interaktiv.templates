import plone.protect.interfaces

from typing import Dict, NoReturn
from plone.dexterity.content import DexterityContent
from plone.restapi.services import Service
from plone import api
from plone.restapi.deserializer import json_body
from zope.interface import alsoProvides
from plone.namedfile.file import NamedBlobImage

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
                self._delete_other_thumbnails(template)

            self._create_and_assign_template_thumbnail(template)

            return create_response(self.request, 200, "Template thumbnail created successfully")

        except Exception as e:
            return create_response(self.request, 500, "An error occurred while processing the template thumbnail.")
            logger.exception("Error proccesing template thumbnail: %s", str(e))

    def _delete_other_thumbnails(self, obj: DexterityContent) -> NoReturn:
        thumbnails = [
            thumbnail for thumbnail in obj.objectValues()
            if getattr(thumbnail, "is_template_thumbnail", False)
        ]
        if thumbnails:
            api.content.delete(objects=thumbnails)

    def _create_and_assign_template_thumbnail(self, template: DexterityContent) -> NoReturn:
        try:
            thumbnail = api.content.create(
                container=template,
                type='Image',
                title="Template Thumbnail",
                id="template-thumbnail",
                **{
                    'is_template_thumbnail': True,
                    'image': NamedBlobImage(
                        data=get_thumbnail(template.absolute_url()),
                        contentType="image/jpeg",
                        filename="Template Thumbnail",
                    ),
                },
            )

            template.template_thumbnail = thumbnail.absolute_url()
            template.reindexObject(idxs=["template_thumbnail"])
        except Exception as e:
            logger.exception("Error creating or assigning template thumbnail: %s", str(e))
            raise
