import argparse
import sys

import six


class CLIParser(object):
    '''CLI Parser that intializes cli parsers for subcommands'''

    def __init__(self,
                 parent_parser=None,
                 command='',
                 help='',
                 description=''):
        self.parent_parser = parent_parser
        self.subcommand_handlers = {}
        self.extra_options_switch = command + '_args'
        # self.extra_options_switch = 'extra'
        self.init_argparse(
            parent_parser=parent_parser,
            command=command,
            help=help,
            description=description)

    def init_argparse(
            self,
            parent_parser=None,
            command='',
            help='',
            description=''):
        if parent_parser is None:
            argparser = argparse.ArgumentParser(description=description)
        else:
            argparser = parent_parser.add_parser(self, command, help=help)
        self.argparser = argparser

    def init_subparsers(self):
        '''Call if this parser is going to have subcommands'''
        subparsers = self.argparser.add_subparsers(
            help='sub-command help',
            dest='subparser_name'
        )

        # Add nargs="*" for zero or more other commands
        self.argparser.add_argument(
            self.extra_options_switch,
            nargs='*',
            help='Other commands'
        )

        self.subparsers = subparsers

    def add_parser(self, handler, command, help=help):
        return self.create_subparser(
            command=command,
            handler=handler,
            help=help
        )

    def create_subparser(self, handler, command, help=''):
        self.subcommand_handlers[command] = handler
        return self.subparsers.add_parser(command, help=help)

    def parse_extra(self, parser, namespace):
        '''This function takes the 'extra' attribute from global
        namespace and re-parses it to create separate namespaces
        for all other chained commands.
        '''
        namespaces = []
        extra = getattr(namespace, self.extra_options_switch)
        while extra:
            n = parser.parse_args(extra)
            extra = getattr(n, self.extra_options_switch)
            namespaces.append(n)
        return namespaces

    def execute(self, parser, options=None):
        extra_options = self.parse_extra(parser, options)
        if options.subparser_name in self.subcommand_handlers:
            handler = self.subcommand_handlers[options.subparser_name]
            handler.execute_command(options, extra_options)
        else:
            print(dir(options))

    def execute_command(self, options, extra_options):
        pass

    def add_arguments(self):
        '''Add arguments to self.argparser'''
        pass

    def main(self, args=None):
        options = self.argparser.parse_args(args=args)
        try:
            self.execute(self.argparser, options)
        except Exception as err:
            print(err)
            six.reraise(type(err), err, sys.exc_info()[2])
