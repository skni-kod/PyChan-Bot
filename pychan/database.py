from typing import Literal, Optional, Union
from nextcord import Guild, Member, User
from nextcord.ext.commands.bot import Bot
from nextcord.message import Message
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, select, insert, update, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import config

engine = create_engine(config.sqlalchemy_db_url, echo=config.database_echo)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class GuildMember(Base):
    __tablename__ = 'guild_members'
    member_id = Column(String, primary_key=True)
    guild_id = Column(String)
    coins = Column(Integer, default=0)


class DiscordUser(Base):
    __tablename__ = 'discord_users'
    user_id = Column(String, primary_key=True)
    osu_username = Column(String)
    osrs_username = Column(String)
    lol_username = Column(String)


class GuildSettings(Base):
    __tablename__ = 'guild_settings'
    guild_id = Column(String, primary_key=True)
    prefix = Column(String, default=config.default_prefix)


class QuizQuestion(Base):
    __tablename__ = 'quiz_questions'
    question_id = Column(Integer, primary_key=True)
    guild_id = Column(String)
    question = Column(String)
    category = Column(String)
    answers = relationship("QuizAnswer")


class QuizAnswer(Base):
    __tablename__ = 'quiz_answers'
    answer_id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('quiz_questions.question_id'))
    answer = Column(String)
    correct = Column(Boolean)


def create_database():
    Base.metadata.create_all(engine)


def get_guild_prefix(_: Bot, message: Message) -> str:
    if not message.guild:
        return ''
    with Session() as s:
        return s.scalar(select(GuildSettings.prefix).where(GuildSettings.guild_id == message.guild.id)) or config.default_prefix


def set_guild_prefix(guild: Guild, prefix: str):
    with Session() as s:
        tag = s.scalar(
            select(GuildSettings.prefix)
            .where(GuildSettings.guild_id == guild.id))

        stmt = None
        if not tag:
            stmt = insert(GuildSettings) \
                .values(guild_id=guild.id, prefix=prefix)
        else:
            stmt = update(GuildSettings) \
                .values(prefix=prefix) \
                .where(GuildSettings.guild_id == guild.id)
        s.execute(stmt)
        s.commit()


def set_game_username(member: Union[User, Member], username: str, game: Literal['osu', 'lol', 'osrs']):
    with Session() as s:
        select_stmt = select(DiscordUser).where(DiscordUser.user_id == member.id)
        user = s.scalar(select_stmt)
        if not user:
            user = DiscordUser(user_id=member.id)
            setattr(user, game + '_username', username)
            s.add(user)
        else:
            setattr(user, game + '_username', username)
        s.commit()


def get_game_username(member: Union[User, Member], game: Literal['osu', 'lol', 'osrs']) -> Optional[str]:
    with Session() as s:
        select_stmt = select(DiscordUser).where(DiscordUser.user_id == member.id)
        user = s.scalar(select_stmt)
        if not user:
            return None
        else:
            return getattr(user, game + '_username')
