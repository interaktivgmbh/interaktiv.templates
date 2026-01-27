from interaktiv.templates.contenttypes.template import ITemplate
from plone.indexer.decorator import indexer


@indexer(ITemplate)
def TemplateThumbnailIndexer(obj: ITemplate) -> str:
    if obj.template_thumbnail:
        return f"{obj.absolute_url()}/@@images/template_thumbnail"
    return ""
