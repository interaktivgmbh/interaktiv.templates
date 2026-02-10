from interaktiv.templates.contenttypes.template import ITemplate
from plone.indexer.decorator import indexer


@indexer(ITemplate)
def TemplateThumbnailIndexer(obj: ITemplate) -> str:
    if obj.template_thumbnail:
        path = "/".join(obj.getPhysicalPath()[2:])
        return f"/{path}/@@images/template_thumbnail"
    return ""
