from zope import schema
from zope.interface import Interface


class IInteraktivTemplatesSchema(Interface):
    thumbnail_user_username = schema.TextLine(
        title='Username',
        description='Username for the thumbnail user',
        required=True,
    )
    thumbnail_user_password = schema.TextLine(
        title='Password',
        description='Password for the thumbnail user',
        required=True,
    )
