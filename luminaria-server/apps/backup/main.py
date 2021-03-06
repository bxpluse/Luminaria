import os
from datetime import date, datetime

from apps.baseapp import App
from common.enums import APP
from constants import DATABASE_CONFIG_NAME, ROOT_DIR


class BackupDatabase(App):

    APP_ID = APP.DB_BACKUP

    def __init__(self):
        super().__init__()
        self.master_db = os.path.join(ROOT_DIR, DATABASE_CONFIG_NAME)

    @staticmethod
    def get_copy_name():
        cur_time = str(date.today()) + '_' + str(datetime.now().strftime("%H-%M"))
        return 'db1_' + cur_time + '.sqlite3'

    def get(self, command):
        if command == 'file-name':
            return {'filename': self.get_copy_name()}

    def blob(self, command):
        if command == 'download':
            return self.master_db
