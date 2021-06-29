from peewee import *

from vars import DB_CONFIG, DB_STATIC, DB_STREAM, DB_DYNAMIC


class ConfigModel(Model):
    class Meta:
        database = DB_CONFIG
        table_name = 'CONFIG_MODEL'

    @classmethod
    def get_table_name(cls):
        return cls._meta.table_name

    @classmethod
    def regenerate(cls):
        cls.drop_table([cls])
        cls.create_table([cls])


class DynamicModel(Model):

    datetime_created = DateTimeField()

    class Meta:
        database = DB_DYNAMIC
        table_name = 'DYNAMIC_MODEL'

    @classmethod
    def get_table_name(cls):
        return cls._meta.table_name

    @classmethod
    def regenerate(cls):
        cls.drop_table([cls])
        cls.create_table([cls])


class StaticModel(Model):
    class Meta:
        database = DB_STATIC
        table_name = 'STATIC_MODEL'

    @classmethod
    def get_table_name(cls):
        return cls._meta.table_name

    @classmethod
    def regenerate(cls):
        cls.drop_table([cls])
        cls.create_table([cls])


class StreamModel(Model):
    class Meta:
        database = DB_STREAM
        table_name = 'STREAM_MODEL'

    @classmethod
    def get_table_name(cls):
        return cls._meta.table_name

    @classmethod
    def regenerate(cls, table):
        cls.drop_table([table])
        cls.create_table([table])
