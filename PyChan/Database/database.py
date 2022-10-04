from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import validates

import datetime

import nextcord
from nextcord.ext import commands


class Database:
    engine = create_engine('sqlite:///Database/PyChan.db')
    Base = declarative_base()
    session = sessionmaker(bind=engine)()

    class Guild(Base):
        __tablename__ = 'guilds'

        guild_id = Column(Integer, primary_key=True)
        name = Column(String)
        join_date = Column(String, default=datetime.datetime.now())
        members_count = Column(Integer)

        @validates('guild_id')
        def validate_id(self, key, id):
            if not (type(id) == int and len(str(id)) == 18):
                raise NameError('[Validates] Guild - id')
            return id

        @validates('name')
        def validate_name(self, key, name):
            if not type(name) == str:
                raise NameError('[Validates] Guild - name')
            return name

        # @validates('members_count')
        # def validate_members_count(self, key, members_count):
        #     if not type(members_count) == int:
        #         raise NameError('[Validates] Guild - members_count')
        #     return id

    class Member(Base):
        __tablename__ = 'members'

        id = Column(Integer, primary_key=True)
        guild_id = Column(Integer, ForeignKey('guilds.guild_id'))
        member_id = Column(Integer)

        @validates('id')
        def validate_address_id(self, key, id):
            if not type(id) == int:
                raise NameError('[Validates] User - id')
            return id

        @validates('member_id')
        def validate_user_id(self, key, user_id):
            if not type(user_id) == int:
                raise NameError('[Validates] User - user_id')
            return user_id

        @validates('guild_id')
        def validate_server_id(self, key, guild_id):
            if not type(guild_id) == int:
                raise NameError('[Validates] User - guild_id')
            return guild_id

    class Settings(Base):
        __tablename__ = 'settings'

        id = Column(Integer, primary_key=True)
        guild_id = Column(Integer, ForeignKey('guilds.guild_id'))
        prefix = Column(String, default='^')

        @validates('id')
        def validate_id(self, key, id):
            if not type(id) == int:
                raise NameError('[Validates] Settings - id')
            return id

        @validates('guild_id')
        def validate_server_id(self, key, guild_id):
            if not type(guild_id) == int:
                raise NameError('[Validates] Settings - guild_id')
            return guild_id

        @validates('prefix')
        def validate_prefix(self, key, prefix):
            if not type(prefix) == str:
                raise NameError('[Validates] Settings - prefix')
            return prefix

    class ServerShiet(Base):
        __tablename__ = 'servers_shiets'

        id = Column(Integer, primary_key=True)
        guild_id = Column(Integer, ForeignKey('guilds.guild_id'))
        value = Column(String)
        miner = Column(String)
        date = Column(String)

        @validates('id')
        def validate_id(self, key, id):
            if not type(id) == int:
                raise NameError('[Validates] ServerShiet - id')
            return id

        @validates('server_id')
        def validate_server_id(self, key, server_id):
            if not type(server_id) == int:
                raise NameError('[Validates] ServerShiet - server_id')
            return server_id

        @validates('value')
        def validate_value(self, key, value):
            if not type(value) == str:
                raise NameError('[Validates] ServerShiet - value')
            return value

        @validates('miner')
        def validate_miner(self, key, miner):
            if not type(miner) == str:
                raise NameError('[Validates] ServerShiet - miner')
            return miner

        @validates('date')
        def validate_date(self, key, date):
            if not type(date) == str:
                raise NameError('[Validates] ServerShiet - date')
            return date

    @classmethod
    def create_database(cls):
        Database.Base.metadata.create_all(Database.engine)

    @classmethod
    def add(cls, _class, **parameters):
        try:
            cls.session.add(_class(**parameters))
            cls.session.commit()
        except Exception as error:
            print('\n[ERROR DB]', *error.args)

    @classmethod
    def add_guild(cls, id):
        try:
            cls.session.add(cls.Guild(guild_id=id))
            cls.session.commit()
        except Exception as error:
            print('\n[ERROR DB]', *error.args)
            print('add g')

    @classmethod
    def add_guild_settings(cls, id):
        try:
            cls.session.add(cls.Settings(guild_id=id))
            cls.session.commit()
        except Exception as error:
            print('\n[ERROR DB]', *error.args)
            print('add g')

    @classmethod
    def add_member(cls, id, g_id):
        try:
            cls.session.add(cls.Member(member_id=id, guild_id=g_id))
            cls.session.commit()
        except Exception as error:
            print('\n[ERROR DB]', *error.args)
            print('add m')

    @classmethod
    def get_all(cls, _class, filter):
        try:
            return cls.session.query(_class).filter(filter).all()
        except Exception as error:
            print('\n[ERROR DB]', *error.args)
        return None

    @classmethod
    def get_first(cls, _class, *filter):
        try:
            return cls.session.query(_class).filter(*filter).first()
        except Exception as error:
            print('\n[ERROR DB]', *error.args)
            print('get')
        return None

    @classmethod
    def update_database(cls, bot):
        for guild in bot.guilds:
            print(guild.name)
            if not Database.get_first(Database.Guild, Database.Guild.guild_id == guild.id):
                Database.add_guild(guild.id)
                guild_db = Database.get_first(
                    Database.Guild, Database.Guild.guild_id == guild.id)
                guild_db.name = guild.name
                guild_db.members_count = guild.member_count
            for member in guild.members:
                if not member.bot:
                    if not Database.get_first(
                            Database.Member, Database.Member.member_id == member.id, Database.Member.guild_id == guild.id):
                        Database.add_member(member.id, guild.id)
            if not Database.get_first(Database.Settings, Database.Settings.guild_id == guild.id):
                Database.add_guild_settings(guild.id)
