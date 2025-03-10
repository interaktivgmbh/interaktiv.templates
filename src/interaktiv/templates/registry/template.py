from zope.interface import Interface
from zope.schema import TextLine
from zope import schema


class ITemplateSchema(Interface):
    thumbnail_user_username = schema.TextLine(
        title='Username',
        description='Username for the thumbnail user',
        required=True,
        default='admin'
    )
    thumbnail_user_password = schema.TextLine(
        title='Password',
        description='Password for the thumbnail user',
        required=True,
        default='admin'
    )