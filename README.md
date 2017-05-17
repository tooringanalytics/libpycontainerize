# Pycontainerize

A Container swarm for Python web-apps.

## Rendering Contexts

Templates are rendered in 2 types of contexts:
  1. Project context
     The context consists of one object called 'project', which contains
     the project-specfific parameters.
  2. Application context
     The context contains the application's parameters, as well as the
     encapsulating project parameters.

## Project Layout:

    - Project Root
        +- apps
        |   +- <app_name>
        |       |
        |       +- appConfig.json
        +- certs: SSL/TLS Certificates for Nginx
        |
        +- projectConfig.json

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
