from nextcord import Guild
from nextcord.ext.commands.bot import Bot
from nextcord.message import Message
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.orm import sessionmaker
import config

class Database:
    Base = declarative_base()
    engine = create_engine(config.sqlalchemy_db_url, echo=True)
    session = sessionmaker(bind=engine)()

    # Stats and settings for guild members
    class GuildMember(Base):
        __tablename__ = 'guild_members'
        member_id = Column(Integer, primary_key=True)
        guild_id = Column(Integer)
        coins = Column(Integer, default=0)

    # Stats and settings for users across all guilds
    class Member(Base):
        __tablename__ = 'members'
        member_id = Column(Integer, primary_key=True)
        osu_username  = Column(String)
        osrs_username = Column(String)
        lol_username  = Column(String)

    class GuildSettings(Base):
        __tablename__ = 'guild_settings'
        guild_id = Column(Integer, primary_key=True)
        prefix = Column(String, default=config.default_prefix)


    @classmethod
    def create_database(cls):
        Database.Base.metadata.create_all(Database.engine)

    @classmethod
    def get_guild_prefix(cls, _: Bot, message: Message) -> str:
        if not message.guild:
            return ''
        return cls.session.scalar(select(cls.GuildSettings.prefix).where(cls.GuildSettings.guild_id == message.guild.id)) or config.default_prefix

    @classmethod
    def set_guild_prefix(cls, guild: Guild, prefix: str):
        cls.session.add(cls.GuildSettings(guild_id=guild.id, prefix=prefix))
        cls.session.commit()

