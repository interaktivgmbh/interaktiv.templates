import logging
from typing import Optional, Any

from plone.dexterity.content import DexterityContent
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
from plone.restapi.services import Service
from plone import api

from interaktiv.templates.helper import common_prefix_length


@implementer(IPublishTraverse)
class InteraktivTemplatesTemplateContainerGet(Service):
    def reply(self) -> str:
        pass

    def get_nearest_template_container(self, content: DexterityContent) -> Optional[DexterityContent]:
        """
        Finds the nearest template container for the given content object.
        The container with the longest common path prefix is selected as the "nearest."

        :param content: The content object for which the closest template container is being searched.
        :return: The nearest template container or None if none is found.
        """
        content_path = content.getPhysicalPath()

        template_containers = api.content.find(portal_type="TemplatesContainer")
        if not containers:
            return None

        nearest_container = None
        max_common = -1

        for container in template_containers:
            container = container.getObject()
            container_path = container.getPhysicalPath()
            common_len = common_prefix_length(content_path, container_path)

            if common_len > max_common:
                max_common = common_len
                nearest_container = container

        return nearest_container
