from constants import ATTR_NAME
from constants import PRJ_ATTR_DOMAINS
from object_config import ObjectConfig


class DomainConfig(ObjectConfig):
    '''Configuration object for domains'''
    config_template_file = 'domainConfigTemplate.json'

    def add_to_project(self, project):
        domains = set(map(lambda x: x[ATTR_NAME], project[PRJ_ATTR_DOMAINS]))
        domains.add(self.obj.name)
        project[PRJ_ATTR_DOMAINS] = list(domains)

    def remove_from_project(self, project):
        domains = set(map(lambda x: x[ATTR_NAME], project[PRJ_ATTR_DOMAINS]))
        domains.remove(self.obj.name)
        project[PRJ_ATTR_DOMAINS] = list(domains)
