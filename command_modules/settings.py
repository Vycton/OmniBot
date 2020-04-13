from omni_data import *
from commands import *


def set_prefix(message):
    server_command_prefixes[message.guild] = message.content
    return "The default prefix for your server is now '" + message.content + "'"


def add_commands(main_module):
    module = CommandModule('settings', 'change my settings', ['Vincent'])
    module.add_command(Command('setprefix', 'set the default prefix indicating a command', ['Vincent'], set_prefix))
    main_module.add_command(module)
