from leaf_node_config import (
    LeafNodeConfig,
)
from constants import (
    ATTR_NAME,
    DOM_ATTR_APPS,
)


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
