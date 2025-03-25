from interaktiv.templates.utilities.helper import get_schema_from_template
from plone.restapi.services.types.get import TypesGet
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


@implementer(IPublishTraverse)
class InteraktivTemplatesTypesGet(TypesGet):

    def reply_for_type(self) -> dict:
        schema = super().reply_for_type()

        return get_schema_from_template(schema)
