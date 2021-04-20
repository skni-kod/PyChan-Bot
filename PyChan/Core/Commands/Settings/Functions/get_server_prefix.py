import discord
from discord.ext import commands

from Database.database import Database

class GetServerPrefix:
    """Class which contains command used to get Bot's prefix
    """
    @staticmethod
    def get_server_prefix(bot, message):
        """Gets server id from sent message

        :param bot: instance of Bot
        :type bot: discord.ext.commands.bot.Bot
        :param message: contains information about message
        :type message: discord.Message
        :return: server's prefix
        :rtype: str
        """

        print(args)
        print(kwargs)

        prefix = None
        try:
            prefix = Database.get_one(Database.db_servers, {'_id': message.guild.id})['settings']['prefix']
        except:
            pass

        if prefix is None:
            return '^'
        return prefix
