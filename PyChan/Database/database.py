from typing import Literal, Optional, Union
from nextcord import Guild, Member, User
from nextcord.ext.commands.bot import Bot
from nextcord.message import Message
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, ForeignKey, create_engine, Column, Integer, String, insert, select, update
from sqlalchemy.orm import relationship, sessionmaker
import config

Base = declarative_base()
engine = create_engine(config.sqlalchemy_db_url, echo=config.database_echo)
session = sessionmaker(bind=engine)()

# Stats and settings for guild members
class GuildMember(Base):
    __tablename__ = 'guild_members'
    member_id = Column(Integer, primary_key=True)
    guild_id = Column(Integer)
    coins = Column(Integer, default=0)

# Stats and settings for users across all guilds
class DiscordUser(Base):
    __tablename__ = 'members'
    member_id = Column(Integer, primary_key=True)
    osu_username  = Column(String)
    osrs_username = Column(String)
    lol_username  = Column(String)

class GuildSettings(Base):
    __tablename__ = 'guild_settings'
    guild_id = Column(Integer, primary_key=True)
    prefix = Column(String, default=config.default_prefix)

class QuizAnswer(Base):
    __tablename__ = 'quiz_answers'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('quiz_questions.id'))
    answer = Column(String)
    correct = Column(Boolean)

class QuizQuestion(Base):
    __tablename__ = 'quiz_questions'
    id = Column(Integer, primary_key=True)
    answers: list[QuizAnswer] = relationship("QuizAnswer")
    guild_id = Column(Integer)
    question = Column(String)
    category = Column(String)

def create_database():
    Base.metadata.create_all(engine)

def get_guild_prefix(_: Bot, message: Message) -> str:
    if not message.guild:
        return ''
    return session.scalar(select(GuildSettings.prefix).where(GuildSettings.guild_id == message.guild.id)) or config.default_prefix

def set_guild_prefix(guild: Guild, prefix: str):
    tag = session.scalar( \
            select(GuildSettings.prefix) \
            .where(GuildSettings.guild_id == guild.id))

    stmt = None
    if not tag:
        stmt = insert(GuildSettings) \
            .values(guild_id=guild.id, prefix=prefix)
    else:
        stmt = update(GuildSettings) \
            .values(prefix=prefix) \
            .where(GuildSettings.guild_id == guild.id)

    session.execute(stmt)
    session.commit()

def set_game_username(member: Union[User, Member], username: str, game: Literal['osu', 'lol', 'osrs']):
    tag = session.query(DiscordUser) \
            .filter(DiscordUser.member_id == member.id).one_or_none()

    if not tag:
        member = DiscordUser(member_id=member.id)
        setattr(member, game + '_username', username)
        session.add(member)
    else:
        tag.osu_username = username

    session.commit()

def get_game_username(member: Union[User, Member], game: Literal['osu', 'lol', 'osrs']) -> Optional[str]:
    tag = session.query(DiscordUser).filter(DiscordUser.member_id == member.id).one_or_none()
    if not tag:
        return None
    else:
        return getattr(tag, game + '_username')

