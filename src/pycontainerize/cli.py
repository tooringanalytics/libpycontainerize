"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mpycontainerize` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``pycontainerize.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``pycontainerize.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
from cli_parser import (
    CLIParser,
)
import click
from factory import (
    create_project,
    create_domain,
    create_app,
    gen,
)


class TestCLIParser(CLIParser):
    pass


class TestCLICommandParser(CLIParser):

    def execute_command(self, options, extra_options):
        print(options.project_name)
        print(options.projects_dir)
        print(options.templates_dir)
        print(options.output_dir)

    def add_arguments(self):
        parser = self.argparser
        parser.add_argument('project_name',
                            help='Name of the project')

        parser.add_argument(
            '-d',
            '--projects-dir',
            help='Projects directory',
        )

        parser.add_argument(
            '-t',
            '--templates-dir',
            help='Templates directory',
        )

        parser.add_argument(
            '-o',
            '--output-dir',
            help='Output directory',
        )
# parser = argparse.ArgumentParser(description='Command description.')
# parser.add_argument('names', metavar='NAME', nargs=argparse.ZERO_OR_MORE,
#                     help="A name of something.")


@click.group('pycontainerize')
def cli():
    pass


@click.group()
def test_grp():
    pass


@click.command()
def test_cmd():
    print('Hello, world')


def main(args=None):
    # app = CLIParser(
    #     command='pycontainerize',
    #     description='Pycontainerize CLI'
    # )
    # app.init_subparsers()
    # test_parent = TestCLIParser(
    #     parent_parser=app,
    #     command='test_cmd_grp',
    #     help='Test Command Group'
    # )
    # test_parent.init_subparsers()
    # test = TestCLICommandParser(
    #     parent_parser=test_parent,
    #     command='test_cmd',
    #     help='Test command'
    # )
    # test.add_arguments()
    # app.main(args=args)
    # test_grp.add_command(test_cmd)
    # cli.add_command(test_grp)
    gen.add_command(create_project)
    gen.add_command(create_domain)
    gen.add_command(create_app)
    cli.add_command(gen)
    cli()
    # args = parser.parse_args(args=args)
    # print(args.names)
