from peewee import *
from playhouse.shortcuts import model_to_dict

from database.base_model import BaseModel


class AppsModel(BaseModel):
    id = CharField(unique=True)
    name = CharField()
    description = CharField(null=True)
    image = CharField(null=True)
    url = CharField()
    order = IntegerField()

    class Meta:
        table_name = 'APPS'

    @staticmethod
    def get_all_apps():
        res = {}
        for app in AppsModel.select():
            res[app.id] = (model_to_dict(app))
        return res
