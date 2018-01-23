from pycontainerize.factory.constants import ATTR_NAME
from pycontainerize.factory.constants import DOM_ATTR_APPS
from pycontainerize.factory.leaf_node_config import LeafNodeConfig


class AppConfig(LeafNodeConfig):
    '''Configuration object for apps'''
    config_template_file = 'appConfigTemplate.json'

    def add_to_domain(self, domain):
        apps = set(map(lambda x: x[ATTR_NAME], domain[DOM_ATTR_APPS]))
        apps.add(self.obj.name)
        domain[DOM_ATTR_APPS] = list(apps)

    def remove_from_domain(self, domain):
        apps = set(map(lambda x: x[ATTR_NAME], domain[DOM_ATTR_APPS]))
        apps.remove(self.obj.name)
        domain[DOM_ATTR_APPS] = list(apps)
