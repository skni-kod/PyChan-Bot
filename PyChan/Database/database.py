from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import validates

import discord
from discord.ext import commands


class DataBase:
    engine = create_engine('sqlite:///PyChan.db')
    Base = declarative_base()
    session = sessionmaker(bind=engine)()

    class Guilds(Base):
        __tablename__ = 'guilds'

        id = Column(Integer, primary_key=True)
        name = Column(String)
        join_date = Column(String)
        members_count = Column(Integer)

        @validates('id')
        def validate_id(self, key, id):
            if not (type(id) == int and len(str(id)) == 18):
                raise NameError('[Validates] Guild - id')
            return id

        @validates('name')
        def validate_name(self, key, name):
            if not type(name) == str:
                raise NameError('[Validates] Guild - name')
            return name

        @validates('members_count')
        def validate_members_count(self, key, members_count):
            if not type(members_count) == int:
                raise NameError('[Validates] Server - members_count')
            return id

    class Member(Base):
        __tablename__ = 'members'

        id = Column(Integer, primary_key=True)
        member_id = Column(Integer)
        server_id = Column(Integer, ForeignKey('guilds.id'))

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
        guild_id = Column(Integer, ForeignKey('guilds.id'))
        prefix = Column(String)

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
        server_id = Column(Integer, ForeignKey('servers.id'))
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
    def add(cls, _class, **parameters):
        try:
            cls.session.add(_class(**parameters))
            cls.session.commit()
        except Exception as error:
            print('\n[ERROR DB]', *error.args)

    Base.metadata.create_all(engine)

    @classmethod
    def get_all(cls, _class, filter):
        try:
            return cls.session.query(_class).filter(filter).all()
        except Exception as error:
            print('\n[ERROR DB]', *error.args)
        return None

    @classmethod
    def get_first(cls, _class, filter):
        try:
            return cls.session.query(_class).filter(filter).first()
        except Exception as error:
            print('\n[ERROR DB]', *error.args)
        return None

    @classmethod
    def check_database(cls, bot):
        for guild in bot.guilds:
            for member in guild.members:
                if not DataBase.get_first(Guild,member_id=member.id):
                    DataBase.add(Member,member_id=member.id,guild_id=guild.id)