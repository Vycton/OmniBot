import discord
from typing import Callable


class CommandError(Exception):
    def __init__(self, command):
        self.command = command

    def get_message(self):
        return "Error in '" + self.command + "':\n"


class UnknownCommandError(CommandError):

    def __init__(self, given_command, command):
        super().__init__(command)
        self.given_command = given_command

    def get_message(self):
        return super().get_message() + self.command + ' is not a known command'


class NoCommandGivenError(CommandError):
    def __init__(self, command):
        super().__init__(command)

    def get_message(self):
        return super().get_message() + 'At least one more command keyword is required'


class CommandHandler:

    def __init__(self, name, help_message, creators):
        self.creators = creators
        self.name = name
        self.help_message = help_message

    def execute(self, message) -> str:
        pass

    def get_command(self, message_contents: [str]):
        pass

    def get_help(self) -> str:
        return self.name + ":\t" + self.help_message


class Command(CommandHandler):

    def __init__(self, name: str, help_message: str, creators: [str], function: Callable[[discord.Message], str]):
        super().__init__(name, help_message, creators)
        self.function = function

    def get_command(self, message_contents: [str]) -> (CommandHandler, str):
        return self, " ".join(message_contents)

    def execute(self, message: discord.Message) -> str:
        return self.function(message)


class CommandModule(CommandHandler):

    def __init__(self, name: str, help_message: str, creators: [str], commands: {str: CommandHandler} = None):
        super().__init__(name, help_message, creators)
        if commands is None:
            commands = {}
        self.commands = commands

    def add_command(self, command: Command):
        self.commands[command.name] = command

    def get_command(self, message_contents: [str]) -> (CommandHandler, str):
        if not message_contents:
            return self, ''
        try:
            command_handler = self.commands[message_contents[0]]
            return command_handler.get_command(message_contents[1:])
        except KeyError:
            raise UnknownCommandError(" ".join(message_contents), self.name)

    def execute(self, message: discord.message) -> str:
        raise NoCommandGivenError(self.name)

    def get_help(self) -> str:

        message = ''
        commands = self.commands.values()
        tab_length = 0

        for command_handler in commands:
            if len(command_handler.name) > tab_length:
                tab_length = len(command_handler.name)

        for command_handler in commands:
            tab = (tab_length - len(command_handler.name) + 1)*' '
            message = message + command_handler.name + tab + ":\t" + command_handler.help_message + '\n'
        return message



