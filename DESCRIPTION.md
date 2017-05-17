WARNING: WORK IN PROGRESS
=========================

# Pycontainerize

A Containerizer for Python web-apps.

## Rendering Contexts

Templates are rendered in 4 types of contexts:

  1. Project context: The context consists of one object called 'project', which contains the project-specific parameters.
  2. Domain context: The context consists of one object called 'domain', which contains the domain-specfific parameters.
  4. Service context: The context consists of:

        - 'service' object containing the service's parameters,
        - 'domain' object, containing the encapsulating domain parameters
        - 'project' object containing the encapsulating project's parameters

  3. Application (App) context: The context consists of:

        - 'app' object containing the application's parameters,
        - 'domain' object, containing the encapsulating domain parameters
        - 'project' object containing the encapsulating project's parameters

## Project Layout:

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

## Template Directory layout:

    - templates
        +- djangoapp: Django app templates
        |
        +- project: Project config file template
        |
        +- services: nginx config templates

## Output Directory Layout:

    - Project Root
        +- apps
        |   +- <app_name>
        +- services
        |
        +- docker-compose.yml
