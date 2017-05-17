#!/usr/bin/env python
'''
Containerize

Create a docker-compose file from a web service specification.
'''
import argparse
import os
import sys
import six

from constants import (
    DEFAULT_PROJECTS_DIR,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_TEMPLATES_DIR,
)
from errors import (
    TemplatesDirNotFound,
    ProjectNotFound,
)
from renderer import (
    Renderer,
)
from project import (
    Project,
)


'''
Templates are rendered in 4 types of contexts:
1. Project context
    The context consists of one object called 'project', which contains
    the project-specific parameters.
2. Domain context
    The context consists of one object called 'domain', which contains
    the domain-specfific parameters.
4. Service context
    The context consists of:
        - 'service' object containing the service's parameters,
        - 'domain' object, containing the encapsulating domain parameters
        - 'project' object containing the encapsulating project's parameters
3. Application (App) context
    The context consists of:
        - 'app' object containing the application's parameters,
        - 'domain' object, containing the encapsulating domain parameters
        - 'project' object containing the encapsulating project's parameters

Project Layout:
    - Project Root
        |
        +- domains
        |    +- <domain.name>
        |       |
        |       +- services
        |       |   +- <service_name>
        |       |   |
        |       |   +- serviceConfig.json
        |       |
        |       +- apps
        |       |   +- <app_name>
        |       |      |
        |       |      +- appConfig.json
        |       +- certs: SSL/TLS Certificates for Nginx
        |
        +- projectConfig.json
        +- networksConfig.json

Template Directory layout:
    - templates
        +- djangoapp: Django app templates
        |
        +- project: Project config file template
        |
        +- services: nginx config templates

Output Directory Layout:
    - Project Root
        +- apps
        |   +- <app_name>
        +- services
        |
        +- docker-compose.yml
'''


class Containerizer(object):
    ''' Main application class '''
    def __init__(self):
        self.parser = self.init_argparse()

    def init_argparse(self):
        parser = argparse.ArgumentParser(
            description='Containerize a project spec'
        )

        parser.add_argument('project_name',
                            help='Name of the project')

        parser.add_argument(
            '-d',
            '--projects-dir',
            help='Projects directory (default: %s)' % DEFAULT_PROJECTS_DIR,
        )

        parser.add_argument(
            '-t',
            '--templates-dir',
            help='Templates directory (default: %s)' % DEFAULT_TEMPLATES_DIR,
        )

        parser.add_argument(
            '-o',
            '--output-dir',
            help='Output directory (default: %s)' % DEFAULT_OUTPUT_DIR,
        )

        return parser

    def load_project(self,
                     project_name,
                     project_dir=DEFAULT_PROJECTS_DIR,
                     output_dir=DEFAULT_OUTPUT_DIR):
        # Load the project from JSON
        project_path = os.path.join(project_dir, project_name)
        project = Project.load(project_path)
        return project

    def render_project(self,
                       project_dir,
                       templates_dir,
                       output_dir):
        ''' Render the templates for this project '''
        # Load the project from JSON
        project = Project.load(project_dir)
        # Create the Jinja2 Renderer
        renderer = Renderer(templates_dir)
        # Now render the templates for the project
        project.render(renderer, output_dir)

    def execute(self, args):
        project = args.project_name

        # Verify the templates dir exists
        if args.templates_dir:
            templates_dir = args.templates_dir
        else:
            templates_dir = DEFAULT_TEMPLATES_DIR

        if not os.path.exists(templates_dir) or \
                not os.path.isdir(templates_dir):
            raise TemplatesDirNotFound(
                'Invalid Templates Directory %s' % templates_dir
            )

        # Verify the project path exists
        if args.projects_dir:
            projects_dir = args.projects_dir
        else:
            projects_dir = DEFAULT_PROJECTS_DIR
        project_path = os.path.join(projects_dir, project)

        if not os.path.exists(project_path) or not os.path.isdir(project_path):
            raise ProjectNotFound('Invalid Project path %s' % project_path)

        # Ensure the output path exists
        if args.output_dir:
            output_dir = args.output_dir
        else:
            output_dir = DEFAULT_OUTPUT_DIR
        output_dir = os.path.join(output_dir, project)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Now create the project from configuration files
        # and templates.
        self.render_project(project_path,
                            templates_dir,
                            output_dir)

    def main(self):
        args = self.parser.parse_args()
        try:
            self.execute(args)
        except Exception as err:
            print(err)
            six.reraise(type(err), err, sys.exc_info()[2])


def main():
    containerizer = Containerizer()
    containerizer.main()


if __name__ == "__main__":
    main()
