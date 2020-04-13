default_command_prefix = '!'

server_command_prefixes = {}

server_command_aliases = {}


def get_prefix(guild):
    return server_command_prefixes.get(guild, default_command_prefix)
