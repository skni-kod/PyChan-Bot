import nextcord
from nextcord.ext import commands
from config import default_prefix
from Database.database import Database


class GetServerPrefix:
    """Class contains command used to get Bot's prefix
    """
    @staticmethod
    def get_server_prefix(bot, message):
        """Gets server id from sent message

        :param bot: instance of Bot
        :type bot: nextcord.ext.commands.bot.Bot
        :param message: contains information about message
        :type message: nextcord.Message
        :return: server's prefix
        :rtype: str
        """

        prefix = None
        try:
            prefix = Database.get_one(Database.db_servers, {'_id': message.guild.id})['settings']['prefix']
        except:
            pass

        if prefix is None:
            return default_prefix
        return prefix
