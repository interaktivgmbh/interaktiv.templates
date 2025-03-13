import logging
from typing import Optional, Any, List, TypedDict

from Products.ZCatalog.interfaces import ICatalogBrain
from plone.dexterity.content import DexterityContent
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
from plone.restapi.services import Service
from plone import api

from interaktiv.templates.utilities.helper import common_prefix_length


class TContainer(TypedDict):
    title: str
    id: str
    url: str
    path: str


class TTemplateContainerData(TypedDict):
    containers: List[TContainer]
    nearest_container: str


class InteraktivTemplatesTemplateContainerGet(Service):
    def reply(self) -> TTemplateContainerData:
        content = api.content.get(path=self.request.form.get("url"))
        if content is None:
            return None

        template_containers = api.content.find(portal_type="TemplatesContainer")
        if not template_containers:
            return None

        containers_list = [self._serialize_container(container) for container in template_containers]

        nearest_container = self._get_nearest_template_container(content, template_containers)

        return {
            "containers": containers_list,
            "nearest_container": nearest_container.absolute_url(),
        }

    def _get_nearest_template_container(self, content: DexterityContent,
                                              template_containers: List[ICatalogBrain]
                                        ) -> Optional[DexterityContent]:
        """
        Finds the nearest template container for the given content object.
        The container with the longest common path prefix is selected as the "nearest."

        :param content: The content object for which the closest template container is being searched.
        :return: The nearest template container or None if none is found.
        """
        if not template_containers:
            return None

        nearest_container = max(
            (container.getObject() for container in template_containers),
            key=common_prefix_length(content.getPhysicalPath(), container.getPhysicalPath()),
            default=None,
        )

        return nearest_container

    def _serialize_container(self, container: ICatalogBrain) -> TContainer:
        if container is None:
            return None

        return {
            "title": container.Title,
            "id": container.getId,
            "url": container.getURL(),
            "path": container.getPath()
        }
