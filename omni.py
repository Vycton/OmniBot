from main_module import *
from secrets import token
import discord


client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message: discord.message):

    if message.author == client.user:
        return

    prefix = get_prefix(message.guild)

    if message.content.startswith(prefix):
        message.content = message.content[len(prefix):].split()
        async with message.channel.typing():
            try:
                command, message.content = main_module.get_command(message.content)
                response = command.execute(message)
            except CommandError as e:
                response = e.get_message() + "\n Use '" + prefix + "help' for more information"
            await message.channel.send(response)


client.run(token)
