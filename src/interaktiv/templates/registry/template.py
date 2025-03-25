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
    basic_auth_enabled = schema.Bool(
        title='Basic Auth Enabled',
        default=False,
    )
    basic_auth_username = schema.TextLine(
        title='Basic Auth Username'
    )
    basic_auth_password = schema.TextLine(
        title='Basic Auth Password'
    )
