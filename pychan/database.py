from typing import Literal, Optional, Union
from nextcord import Guild, Member, User
from nextcord.ext.commands.bot import Bot
from nextcord.message import Message
from sqlalchemy import ForeignKey, create_engine, insert, select, update
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, sessionmaker
import config

engine = create_engine(config.sqlalchemy_db_url, echo=config.database_echo)

def session() -> Session:
    return Session(engine)


class Base(DeclarativeBase):
    pass

# Stats and settings for guild members


class GuildMember(Base):
    __tablename__ = 'guild_members'
    member_id: Mapped[int] = mapped_column(primary_key=True)
    guild_id: Mapped[int] = mapped_column()
    coins: Mapped[int] = mapped_column(default=0)

# Stats and settings for users across all guilds


class DiscordUser(Base):
    __tablename__ = 'discord_users'
    user_id: Mapped[int] = mapped_column(primary_key=True)
    osu_username: Mapped[Optional[str]] = mapped_column()
    osrs_username: Mapped[Optional[str]] = mapped_column()
    lol_username: Mapped[Optional[str]] = mapped_column()


class GuildSettings(Base):
    __tablename__ = 'guild_settings'
    guild_id: Mapped[int] = mapped_column(primary_key=True)
    prefix: Mapped[str] = mapped_column(default=config.default_prefix)


class QuizQuestion(Base):
    __tablename__ = 'quiz_questions'
    question_id: Mapped[int] = mapped_column(primary_key=True)
    answers: Mapped[list["QuizAnswer"]] = relationship()
    guild_id: Mapped[int] = mapped_column()
    question: Mapped[str] = mapped_column()
    category: Mapped[str] = mapped_column()


class QuizAnswer(Base):
    __tablename__ = 'quiz_answers'
    answer_id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(
        ForeignKey('quiz_questions.question_id'))
    answer: Mapped[str] = mapped_column()
    correct: Mapped[bool] = mapped_column()


def create_database():
    Base.metadata.create_all(engine)


def get_guild_prefix(_: Bot, message: Message) -> str:
    if not message.guild:
        return ''
    with session() as s:
        return s.scalar(select(GuildSettings.prefix).where(GuildSettings.guild_id == message.guild.id)) or config.default_prefix


def set_guild_prefix(guild: Guild, prefix: str):
    with session() as s:
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
    with session() as s:
        select_stmt = select(DiscordUser).where(DiscordUser.user_id == member.id)
        user = s.scalar(select_stmt)
        if not user:
            user = DiscordUser(user_id=member.id)
            setattr(user, game + '_username', username)
            s.add(user)
        else:
            user.osu_username = username
        s.commit()


def get_game_username(member: Union[User, Member], game: Literal['osu', 'lol', 'osrs']) -> Optional[str]:
    with session() as s:
        select_stmt = select(DiscordUser).where(DiscordUser.user_id == member.id)
        user = s.scalar(select_stmt)
        if not user:
            return None
        else:
            return getattr(user, game + '_username')
