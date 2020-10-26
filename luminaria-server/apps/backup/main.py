import os
from shutil import copyfile
from datetime import date, datetime
from constants import BACKUP_DIR
from vars import ROOT_DIR, DATABASE_NAME
from apps.baseapp import App


class BackupDatabase(App):

    APP_ID = 'db-backup'

    def __init__(self):
        super().__init__()
        self.dir_path = os.path.join(ROOT_DIR, BACKUP_DIR)
        self.master_db = os.path.join(ROOT_DIR, DATABASE_NAME)
        os.makedirs(self.dir_path, exist_ok=True)

    def run(self, **kwargs):
        super().start()
        file_name = self.get_copy_name()
        backup_file = os.path.join(self.dir_path, file_name)
        copyfile(self.master_db, backup_file)
        super().stop()

    @staticmethod
    def get_copy_name():
        cur_time = str(date.today()) + '_' + str(datetime.now().strftime("%H-%M"))
        return 'database_' + cur_time + '.sqlite3'