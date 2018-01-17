from constants import ATTR_NAME
from constants import DOM_ATTR_SERVICES
from constants import PRJ_ATTR_SERVICES
from leaf_node_config import LeafNodeConfig


class ServiceConfig(LeafNodeConfig):
    '''Configuration object for services'''
    config_template_file = 'serviceConfigTemplate.json'

    def add_to_project(self, project):
        services = set(map(lambda x: x[ATTR_NAME], project[PRJ_ATTR_SERVICES]))
        services.add(self.obj.name)
        project[PRJ_ATTR_SERVICES] = list(services)

    def remove_from_project(self, project):
        services = set(map(lambda x: x[ATTR_NAME], project[PRJ_ATTR_SERVICES]))
        services.remove(self.obj.name)
        project[PRJ_ATTR_SERVICES] = list(services)

    def add_to_domain(self, domain):
        services = set(map(lambda x: x[ATTR_NAME], domain[DOM_ATTR_SERVICES]))
        services.add(self.obj.name)
        domain[DOM_ATTR_SERVICES] = list(services)

    def remove_from_domain(self, domain):
        services = set(map(lambda x: x[ATTR_NAME], domain[DOM_ATTR_SERVICES]))
        services.remove(self.obj.name)
        domain[DOM_ATTR_SERVICES] = list(services)
