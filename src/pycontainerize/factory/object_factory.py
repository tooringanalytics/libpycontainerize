from constants import (
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
        project[PRJ_ATTR_DOMAINS].append(domain_config.obj.name)
        return domain_config.to_python()

    def remove_domain(self, project, domain_name):
        pass

    def create_app(self, domain, app_config):
        domain[DOM_ATTR_APPS].append(app_config.obj.name)
        return app_config.to_python()

    def remove_app(self, domain, app_name):
        pass

    def create_project_service(self, project, service_config):
        project[PRJ_ATTR_SERVICES].append(service_config.obj.name)
        return service_config.to_python()

    def remove_project_service(self, project, service_name):
        pass

    def create_domain_service(self, domain, service_config):
        domain[DOM_ATTR_SERVICES].append(service_config.obj.name)
        return service_config.to_python()

    def remove_domain_service(self, domain, service_name):
        pass
