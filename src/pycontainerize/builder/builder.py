import click


@click.command()
@click.argument('project_name')
def build_project(project_name):
    pass


@click.group()
def builder():
    pass


if __name__ == '__main__':
    builder.add_command(build_project)
