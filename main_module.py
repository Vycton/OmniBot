import importlib
import pkgutil
from commands import *
from omni_data import *


def __load_modules(package_name):
    command_dictionary = {}
    package = __import__(package_name, fromlist=[" "])

    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):

        if ispkg:
            command_dictionary.update(__load_modules(package_name + '.' + modname))
        else:

            module = importlib.import_module('.' + modname, package_name)
            try:
                module.add_commands(main_module)
            except AttributeError:
                pass

    return command_dictionary


def help_message(message):
    content = message.content.split()

    if not content:
        return "These are all top-level commands, type '" + \
               get_prefix(message.guild) + "help <command name>' for more information on a specific command.\n```" + \
               main_module.get_help() + '```'

    command, _ = main_module.get_command(content)

    if type(command) is CommandModule:
        return "Here are the commands in the module '" + command.name + "', type '" + \
               get_prefix(message.guild) + "help <command name>' for more information on a specific command.\n```" + \
               command.get_help() + '```'

    return command.get_help()


__help_command = Command('help', 'displays help messages', ['Vincent'], help_message)
main_module = CommandModule('Omni', 'Multi-purpose discord bot', [], {})
main_module.add_command(__help_command)
__load_modules('command_modules')
