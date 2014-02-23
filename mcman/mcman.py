""" mcman main module. """
import argparse
from mcman.plugins import Plugins
from mcman.servers import Servers


def negative(argument):
    """ Turn a number negative. """
    return -abs(int(argument))


def setup_server_commands(sub_parsers):
    """ Setup the commands and subcommands for server. """
    # The server command parser
    parser = sub_parsers.add_parser(
        'server', aliases=['s'],
        help='Manage server jars',
        description='Download, identify and list Minecraft server jars.')
    parser.set_defaults(command=Servers)
    # The server sub commands
    sub_parsers = parser.add_subparsers(title='subcommands')
    # servers, sub command of server
    servers_parser = sub_parsers.add_parser(
        'servers', aliases=['s'],
        help='List available servers.',
        description='List all server jars available for download.')
    servers_parser.set_defaults(subcommand='servers')
    # channels, sub command of server
    channels_parser = sub_parsers.add_parser(
        'channels', aliases=['c'],
        help='List channels for the specified server.',
        description='List all available channels for the server specified.')
    channels_parser.set_defaults(subcommand='channels')
    channels_parser.add_argument(
        'server', help='The server to get channels for.')
    # versions, sub command of server
    versions_parser = sub_parsers.add_parser(
        'versions', aliases=['v'],
        help='List versions for the specified server.',
        description='List all available versions for the server specified, '
                    + 'or only the versions in the specified channel.')
    versions_parser.set_defaults(subcommand='versions')
    versions_parser.add_argument(
        'server', help='The server to get versions for.')
    versions_parser.add_argument(
        'channel', nargs='?', help='The channel to get versions for.')
    # download, sub command of server
    download_parser = sub_parsers.add_parser(
        'download', aliases=['d'],
        help='Download the newest version of the server.',
        description='Download the newest, the newest in the channel, or the '
                    + 'specified version of the jar.')
    download_parser.set_defaults(subcommand='download')
    download_parser.add_argument(
        'server', help='The server to download.')
    download_parser.add_argument(
        'channel', nargs='?', help='The channel to dowload from.')
    download_parser.add_argument(
        'version', nargs='?', help='The specific version to download.')
    # identify, sub command of server
    identify_parser = sub_parsers.add_parser(
        'identify', aliases=['i'],
        help='Identify the server and version of the jar file.',
        description='Identifies the server, version and possibly channel of '
                    + 'the jar file specified.')
    identify_parser.set_defaults(subcommand='identify')
    identify_parser.add_argument(
        'jar', type=argparse.FileType('rb', 0),
        help='The jar file to identify.')

    return parser


def setup_plugin_commands(sub_parsers):
    """ Setup the commands and subcommands for plugin. """
    # The plugin command parser
    parser = sub_parsers.add_parser(
        'plugin', aliases=['p'],
        help='Manage plugins',
        description='Find, download and update plugins.')
    parser.set_defaults(command=Plugins)

    # Base URL
    parser.add_argument(
        '--base-url', metavar='base-url', default='http://api.bukget.org/3/',
        help='The base URL to use for BukGet')

    # The plugin sub commands
    sub_parsers = parser.add_subparsers()
    # search, sub command of plugin
    search_parser = sub_parsers.add_parser(
        'search', aliases=['s'],
        help='Search for a plugin',
        description='Search for a plugin using partial matching of the name.')
    search_parser.set_defaults(subcommand='search')
    search_parser.add_argument(
        'query', help='Search query.')
    # info, sub command of plugin
    info_parser = sub_parsers.add_parser(
        'info', aliases=['i'],
        help='Get info about a plugin(s)',
        description='Get info about one, or more plugins.')
    info_parser.set_defaults(subcommand='info')
    info_parser.add_argument(
        'plugins', metavar='plugin', type=str, nargs='+',
        help='Plugin(s) to get info for.')
    # download, sub command of plugin
    download_parser = sub_parsers.add_parser(
        'download', aliases=['d'],
        help='Download a plugin(s)',
        description='Download the specified plugin(s). A version can be '
                    + 'specified by appending "#<version>" to the plugin name')
    download_parser.set_defaults(subcommand='download')
    download_parser.add_argument(
        'plugins', metavar='plugin', type=str, nargs='+',
        help='Plugin(s) to download, and extract if they are zipped.')
    # update, sub command of plugin
    update_parser = sub_parsers.add_parser(
        'update', aliases=['u'],
        help='Update a plugin(s)',
        description='Update the specified plugins, or all.')
    update_parser.set_defaults(subcommand='update')
    update_parser.add_argument(
        'plugins', metavar='plugin', type=str, nargs='*',
        help='Plugin(s) update.')
    # list, sub command of plugin
    list_parser = sub_parsers.add_parser(
        'list', aliases=['l'],
        help='List installed plugins',
        description='List installed plugins, their versions, and the newest '
                    + 'version.')
    list_parser.set_defaults(subcommand='list')

    return parser


def main():
    """ Main function. """
    # The top level command
    parser = argparse.ArgumentParser(
        description='Manage Minecraft server jars and plugins',
        epilog='Powered by BukGet and SpaceGDN')

    # Commands that can be used for all sub commands
    parser.add_argument(
        '--version',
        help='Show the version of mcman, then proceede normally',
        action='store_true')
    parser.add_argument(
        '--user-agent',
        metavar='agent',
        type=str,
        default='mcman 0.1',
        help='Alternative user agent to report to BukGet and SpaceGDN')
    # Head and tail, they are mutually exclusive
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--head',
        metavar='size',
        type=int,
        dest='size',
        nargs='?',
        default=80,
        const=10,
        help='How many entries that should be displayed, from the top')
    group.add_argument(
        '--tail',
        metavar='size',
        type=negative,
        dest='size',
        nargs='?',
        default=80,
        const=-10,
        help='How many entries that should be displayed, from the bottom')

    # The sub commands, plugin and server
    sub_parsers = parser.add_subparsers(title='subcommands')

    server_parser = setup_server_commands(sub_parsers)
    plugin_parser = setup_plugin_commands(sub_parsers)

    args = parser.parse_args()
    if args.version:
        print('Version: {}'.format('uknown'))
    if not 'command' in args:
        parser.print_help()
        return
    if not 'subcommand' in args:
        if args.command is Plugins:
            plugin_parser.print_help()
        elif args.command is Servers:
            server_parser.print_help()
        else:
            return
    args.command(args)

if __name__ == '__main__':
    main()