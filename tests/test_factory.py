import unittest
from pycontainerize import (
    TypeConfig,
    ProjectConfig,
    DomainConfig,
    ObjectFactory,
)
from pycontainerize.errors import InvalidTypeError


class FactoryTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestTypeConfig(FactoryTestCase):

    def test_invalid(self):
        try:
            type_config = TypeConfig('randommm')
            type_config.initialize()
        except InvalidTypeError:
            self.assertTrue(True)
            pass

    def test_default_values(self):
        type_config = TypeConfig('ContainerDict')
        type_config.initialize()
        config = type_config.to_python()
        self.assertTrue('image' in config)
        self.assertEquals(config['image'], '<docker-container-image>')
        self.assertTrue('alias' in config)
        self.assertEquals(config['alias'], '<instance-alias>')

    def test_composite(self):
        type_config = TypeConfig('DeployDict')
        type_config.initialize()
        config = type_config.to_python()
        self.assertTrue('docker' in config)
        self.assertTrue(type(config['docker']) is dict)
        docker = config['docker']
        self.assertTrue('certs_dir' in docker)
        self.assertEquals(docker['certs_dir'], '/home/docker/certs')

    def test_project(self):
        project_config = ProjectConfig()
        project_config.initialize()
        project_config.obj.name = 'test_project'
        project_config.obj.version = '1.1.4'

        factory = ObjectFactory()
        project = factory.create_project(project_config)
        self.assertTrue('name' in project)
        self.assertEquals(project['name'], 'test_project')
        self.assertTrue('version' in project)
        self.assertEquals(project['version'], '1.1.4')
        self.assertTrue('domains' in project)
        self.assertEquals(project['domains'], [])
        self.assertTrue('deploy' in project)
        self.assertTrue(type(project['deploy']) is dict)
        deploy = project['deploy']
        self.assertTrue('docker' in deploy)
        self.assertTrue(type(deploy['docker']) is dict)
        docker = deploy['docker']
        self.assertTrue('certs_dir' in docker)
        self.assertEquals(docker['certs_dir'], '/home/docker/certs')


class TestDomainConfig(FactoryTestCase):

    def setUp(self):
        project_config = ProjectConfig()
        project_config.initialize()
        project_config.obj.name = 'test_project'
        project_config.obj.version = '1.1.4'

        factory = ObjectFactory()
        project = factory.create_project(project_config)

        self.factory = factory
        self.project = project

    def tearDown(self):
        pass

    def test_domain(self):
        domain_config = DomainConfig()
        domain_config.initialize()
        domain_config.obj.name = 'test.domain.com'
        domain = self.factory.create_domain(self.project, domain_config)
        self.assertTrue('name' in domain)
        self.assertTrue('server_name' in domain)
        self.assertTrue('server_fqdn' in domain)
        self.assertTrue('server_secure_url' in domain)
        self.assertTrue('default_server' in domain)
        self.assertTrue('ssl_certificate' in domain)
        self.assertTrue('ssl_certificate_key' in domain)
        self.assertTrue('apps' in domain)
        self.assertTrue('services' in domain)
        self.assertTrue('test.domain.com' in set(self.project['domains']))


class TestAppConfig(FactoryTestCase):

    def setUp(self):
        project_config = ProjectConfig()
        project_config.initialize()
        project_config.obj.name = 'test_project'
        project_config.obj.version = '1.1.4'

        factory = ObjectFactory()
        project = factory.create_project(project_config)

        self.factory = factory
        self.project = project

        domain_config = DomainConfig()
        domain_config.initialize()
        domain_config.obj.name = 'test.domain.com'
        domain = self.factory.create_domain(self.project, domain_config)
        self.domain = domain

    def tearDown(self):
        pass
