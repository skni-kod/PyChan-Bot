import discord
from discord.ext import commands

from PyChan.Database.database import Database


def get_server_prefix(bot, message):
    try:
        prefix = Database.get_one(Database.db_servers, {'_id': message.guild.id})['settings']['prefix']
    except:
        pass

    if prefix is None:
        return '^'
    return prefix
