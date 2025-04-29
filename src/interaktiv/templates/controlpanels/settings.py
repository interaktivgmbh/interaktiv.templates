from typing import Dict, Any

import plone.api as api
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from interaktiv.templates.registry.template import IInteraktivTemplatesSchema


class InteraktivTemplatesSettingsView(BrowserView):
    template = ViewPageTemplateFile("templates/settings.pt")

    def __call__(self) -> str:
        form = self.request.form

        if 'submit' in form:
            self.set_settings(self.request.form)

        return self.template(self)

    @staticmethod
    def get_registry_record_value(name: str) -> Any:
        return api.portal.get_registry_record(name, IInteraktivTemplatesSchema, default="")

    @staticmethod
    def set_settings(form: Dict) -> None:
        basic_auth_fields = [
            'basic_auth_username',
            'basic_auth_password'
        ]
        for field in basic_auth_fields:
            if field in form.keys():
                api.portal.set_registry_record(name=field, value=form[field], interface=IInteraktivTemplatesSchema)
