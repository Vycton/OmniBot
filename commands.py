import discord


class _CommandError(Exception):
    def __init__(self, command_name):
        self.command_name = command_name

    def get_message(self):
        if not self.command_name:
            return "Error:\n"
        return "Error in '" + self.command_name + "':\n"


class _UnknownCommandError(_CommandError):

    def __init__(self, given_command, command_name):
        super().__init__(command_name)
        self.given_command = given_command

    def get_message(self):
        return super().get_message() + self.given_command + ' is not a known command'


class _NoCommandGivenError(_CommandError):
    def __init__(self, command_name):
        super().__init__(command_name)

    def get_message(self):
        return super().get_message() + 'At least one more command keyword is required'


class _NotEnoughArgumentsError(_CommandError):

    def __init__(self, command_name, missing_arguments):
        super().__init__(command_name)
        self.missing_arguments = missing_arguments

    def get_message(self):
        message = super().get_message() + 'The following arguments are required:\n```'
        message = message + _format_help(self.missing_arguments) + '```'
        return message


class WrongArgumentError(_CommandError):

    def __init__(self, argument, dev_message=''):
        super().__init__('')
        self.argument = argument
        self.dev_message = dev_message

    def get_message(self):
        message = 'The following argument is incorrect:\n```'
        message = message + _format_help([self.argument])
        message = message + '\n' + self.dev_message + '```'
        return message


class _CommandElement:
    def __init__(self, name, help_message):
        self.name = name
        self.help_message = help_message


class Argument(_CommandElement):

    def __init__(self, name, help_message, optional=False, required_type=None):
        optional_help = '(optional) ' if optional else ''
        super().__init__(name,  optional_help + help_message)
        self.required_type = required_type
        self.optional = optional


class _CommandHandler(_CommandElement):

    def __init__(self, name, help_message, creators):
        super().__init__(name, help_message)
        self.creators = creators

    def execute(self, message) -> str:
        pass

    def get_command(self, message_contents: [str]):
        pass

    def get_help(self) -> str:
        return self.name + ":\t" + self.help_message


class Command(_CommandHandler):

    def __init__(self, name: str, help_message: str, creators: [str], function, arguments=None):
        super().__init__(name, help_message, creators)
        if arguments is None:
            arguments = []
        self.arguments = arguments
        self.function = function

    def get_command(self, message_contents: [str]) -> (_CommandHandler, str):
        return self, " ".join(message_contents)

    def execute(self, message: discord.Message) -> str:
        given_arguments = message.content.split()
        if len(given_arguments) < len([a for a in self.arguments if not a.optional]):
            raise _NotEnoughArgumentsError(self.name, self.arguments)
        try:
            return self.function(message)
        except WrongArgumentError as e:
            e.command_name = self.name
            raise e

    def get_help(self) -> str:
        return self.name + ' ' + ' '.join(['<' + a.name + '>' for a in self.arguments]) + ': ' + self.help_message + '\n' \
               + _format_help(self.arguments)


class CommandModule(_CommandHandler):

    def __init__(self, name: str, help_message: str, creators: [str], commands: {str: _CommandHandler} = None):
        super().__init__(name, help_message, creators)
        if commands is None:
            commands = {}
        self.commands = commands

    def add_command(self, command: Command):
        self.commands[command.name] = command

    def get_command(self, message_contents: [str]) -> (_CommandHandler, str):
        if not message_contents:
            return self, ''
        try:
            command_handler = self.commands[message_contents[0]]
            return command_handler.get_command(message_contents[1:])
        except KeyError:
            raise _UnknownCommandError(" ".join(message_contents), self.name)

    def execute(self, message: discord.message) -> str:
        raise _NoCommandGivenError(self.name)

    def get_help(self) -> str:
        return _format_help(self.commands.values())


def _format_help(command_elements):
    message = ''
    tab_length = 0
    for command_element in command_elements:
        if len(command_element.name) > tab_length:
            tab_length = len(command_element.name)
    for command_element in command_elements:
        tab = (tab_length - len(command_element.name) + 1) * ' '
        message = message + command_element.name + tab + ":\t" + command_element.help_message + '\n'
    return message
