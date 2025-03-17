from typing import Optional, List, TypedDict

from Products.ZCatalog.interfaces import ICatalogBrain
from plone import api
from plone.dexterity.content import DexterityContent
from plone.restapi.services import Service

from interaktiv.templates.contenttypes.templatescontainer import TemplatesContainer
from interaktiv.templates.utilities.helper import common_prefix_length


class TTemplatesContainer(TypedDict):
    title: str
    id: str
    url: str
    path: str


class TTemplateContainerData(TypedDict):
    containers: List[TTemplatesContainer]
    nearest_container: str


class InteraktivTemplatesTemplateContainerGet(Service):
    def reply(self) -> Optional[TTemplateContainerData]:
        print(self.request)
        content = api.content.get(path=self.request.form.get("url"))
        if content is None:
            return None

        templates_containers = api.content.find(portal_type="TemplatesContainer")
        if not templates_containers:
            return None

        nearest_container = self._get_nearest_template_container(content, templates_containers)

        return {
            "containers": [self._serialize(brain) for brain in templates_containers],
            "nearest_container": nearest_container.absolute_url(),
        }

    @staticmethod
    def _get_nearest_template_container(content: DexterityContent, templates_containers: List[ICatalogBrain]) -> \
            Optional[TemplatesContainer]:
        """ The container with the longest common path prefix is selected as the "nearest". """
        if not templates_containers:
            return None

        def get_common_length(container: TemplatesContainer) -> int:
            return common_prefix_length(content.getPhysicalPath(), container.getPhysicalPath())

        nearest_container = max(
            (c.getObject() for c in templates_containers),
            key=get_common_length,
            default=None,
        )

        return nearest_container

    @staticmethod
    def _serialize(brain: ICatalogBrain) -> TTemplatesContainer:
        return {"title": brain.Title, "id": brain.getId, "url": brain.getURL(), "path": brain.getPath()}
