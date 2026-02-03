from plone.indexer.decorator import indexer

from interaktiv.templates.contenttypes.template import ITemplate


@indexer(ITemplate)
def TemplateThumbnailIndexer(obj: ITemplate) -> str:
    if obj.template_thumbnail:
        path = '/'.join(obj.getPhysicalPath()[2:])
        return f'/{path}/@@images/template_thumbnail'
    return ''
