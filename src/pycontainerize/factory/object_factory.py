from constants import (
    ATTR_NAME,
    PRJ_ATTR_DOMAINS,
    PRJ_ATTR_SERVICES,
    DOM_ATTR_APPS,
    DOM_ATTR_SERVICES,
)


class ObjectFactory(object):
    '''Factory class for creating various types of configuration files'''

    def create_project(self, project_config):
        '''Creates a project from the given configuration template'''
        return project_config.to_python()

    def create_domain(self, project, domain_config):
        domain_config.add_to_project(project)
        return domain_config.to_python()

    def remove_domain(self, project, domain_config):
        domain_config.remove_from_project(project)

    def create_app(self, domain, app_config):
        app_config.add_to_domain(domain)
        return app_config.to_python()

    def remove_app(self, domain, app_config):
        app_config.remove_from_domain(domain)

    def create_project_service(self, project, service_config):
        service_config.add_to_project(project)
        return service_config.to_python()

    def remove_project_service(self, project, service_config):
        service_config.remove_from_project(project)

    def create_domain_service(self, domain, service_config):
        service_config.add_to_domain(domain)
        return service_config.to_python()

    def remove_domain_service(self, domain, service_config):
        service_config.remove_from_domain(domain)
