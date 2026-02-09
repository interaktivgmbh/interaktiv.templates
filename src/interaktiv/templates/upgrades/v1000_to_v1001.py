from Products.CMFCore.CatalogTool import CatalogTool
from Products.GenericSetup.tool import SetupTool
from plone import api


# noinspection PyUnusedLocal
def upgrade(site_setup: SetupTool | None = None) -> None:
    catalog: CatalogTool = api.portal.get_tool("portal_catalog")

    # change index meta_type to FieldIndex
    index_obj = catalog._catalog.getIndex("template_thumbnail")
    if index_obj.meta_type != "FieldIndex":
        catalog.delIndex("template_thumbnail")
        catalog.addIndex("template_thumbnail", "FieldIndex")

    # automatic reindexing for templates
    brains = catalog(portal_type="Template")
    for brain in brains:
        template_obj = brain.getObject()
        template_obj.reindexObject()
