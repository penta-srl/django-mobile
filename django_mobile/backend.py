from django.conf import settings
from django.template import TemplateDoesNotExist
from django.template.backends.base import BaseEngine

from django_mobile import get_flavour
from django_mobile.compat import template_loader


class DjangoMobileBackend(BaseEngine):

    # Name of the subdirectory containing the templates for this engine
    # inside an installed application.
    _template_backends = None

    def __init__(self, params):
        params = params.copy()
        options = params.pop("OPTIONS").copy()
        super().__init__(params)

    def from_string(self, template_code):
        pass

    def _prepare_template_name(self, template_name):
        """Prepare the template name taking into consideration the flavor."""
        template_name = "%s/%s" % (get_flavour(), template_name)
        if settings.FLAVOURS_TEMPLATE_PREFIX:
            template_name = settings.FLAVOURS_TEMPLATE_PREFIX + template_name
        return template_name

    def get_template(self, template_name, skip=None):
        """Iterate over configured Backends
        and return the value from the first one to find the template.
        """
        template_name = self._prepare_template_name(template_name)
        for loader in self.template_backends:
            try:
                return loader.get_template(template_name, skip)
            except TemplateDoesNotExist:
                pass
        raise TemplateDoesNotExist("Tried %s" % template_name)

    @property
    def template_backends(self):
        if not self._template_backends:
            loaders = []
            for loader_name in settings.FLAVOURS_TEMPLATE_BACKENDS:
                loader = template_loader(loader_name)
                if loader is not None:
                    loaders.append(loader)
            self._template_backends = tuple(loaders)
        return self._template_backends
