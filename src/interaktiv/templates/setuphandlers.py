from typing import NoReturn

from Products.CMFPlone.Portal import PloneSite
from plone import api
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

from interaktiv.templates.registry.template import IInteraktivTemplatesSchema
from interaktiv.templates.utilities.helper import generate_secure_password


def create_or_update_template_thumbnail_user():
    username = api.portal.get_registry_record('thumbnail_user_username', interface=IInteraktivTemplatesSchema)
    password = api.portal.get_registry_record('thumbnail_user_password', interface=IInteraktivTemplatesSchema)

    user = api.user.get(userid=username)
    if user:
        user.setSecurityProfile(password=password)

    else:
        api.user.create(
            username=username,
            password=password,
            email='thumbnail-user@tmp.tmp',
            roles=['Reader']
        )


# noinspection PyUnusedLocal
def post_install(context: PloneSite) -> NoReturn:
    registry = getUtility(IRegistry)
    registry.registerInterface(IInteraktivTemplatesSchema)

    api.portal.set_registry_record(name='thumbnail_user_username', value='thumbnail-user', interface=IInteraktivTemplatesSchema)
    api.portal.set_registry_record(name='thumbnail_user_password', value=generate_secure_password(),
                                   interface=IInteraktivTemplatesSchema)

    create_or_update_template_thumbnail_user()
