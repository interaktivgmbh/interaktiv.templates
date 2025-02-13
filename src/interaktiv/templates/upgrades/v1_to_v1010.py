from typing import Optional, NoReturn

from Products.GenericSetup.tool import SetupTool

from interaktiv.framework.storage import storage


def upgrade(site_setup: Optional[SetupTool] = None) -> NoReturn:
    behavior = 'interaktiv.templates.behaviors.thumbnail.IThumbnailBehavior'
    storage.set_behavior(behavior, 'Image')