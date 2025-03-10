from typing import NoReturn

from Products.CMFPlone.Portal import PloneSite
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

from interaktiv.templates.registry.template import ITemplateSchema
from interaktiv.templates.utilities.helper import generate_secure_password
from plone import api


def create_template_thumbnail_user():
    if not api.user.get(userid='thumbnail-user'):
        api.user.create(
            username=api.portal.get_registry_record('thumbnail_user_username', interface=ITemplateSchema),
            password=api.portal.get_registry_record('thumbnail_user_password', interface=ITemplateSchema),
            email='thumbnail-user@tmp.tmp',
            roles=['Reader']
        )


# noinspection PyUnusedLocal
def post_install(context: PloneSite) -> NoReturn:
    registry = getUtility(IRegistry)
    registry.registerInterface(ITemplateSchema)

    api.portal.set_registry_record(name='thumbnail_user_username', value='thumbnail-user', interface=ITemplateSchema)
    api.portal.set_registry_record(name='thumbnail_user_password', value=generate_secure_password(),
                                   interface=ITemplateSchema)

    create_template_thumbnail_user()
