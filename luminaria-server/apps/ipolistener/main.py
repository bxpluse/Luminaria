import threading

import requests
from apscheduler.schedulers.background import BackgroundScheduler

from apps.baseapp import App
from common.enums import APPSTATUS
from common.enums import APPTYPE
from config import SCHEDULER_TIME_ZONE
from database.ipo_strings_model import IPOStringModel
from database.local_config_model import LocalConfigModel


class IPOListener(App):
    APP_ID = 'ipo-listener'

    def __init__(self):
        super().__init__(app_type=APPTYPE.STREAMING)
        self.scheduler = BackgroundScheduler({'apscheduler.timezone': SCHEDULER_TIME_ZONE})
        self.scheduler.start()
        self.MAIN_SITE = LocalConfigModel.retrieve("IPO_CALENDAR_MARKETWATCH")
        self.SITES = [self.MAIN_SITE,
                      LocalConfigModel.retrieve("IPO_CALENDAR_YAHOO"),
                      LocalConfigModel.retrieve("IPO_CALENDAR_NASDAQ")]

    def run(self):
        super().start()
        job = self.scheduler.add_job(self.search, trigger='cron', hour='*/6')
        try:
            self.search()
        except Exception as e:
            self.status = APPSTATUS.ERROR
            job.remove()
            self.info("ERROR: " + (repr(e)))
            self.info("Jobs after catching exception: " + str(self.scheduler.get_jobs()))
            self.info("Restarting ...")
            timer = threading.Timer(60, self.run)
            timer.start()

    def search(self):
        terms = IPOStringModel.get_all_not_found_strings()
        response = requests.get(self.MAIN_SITE)
        cleaned = response.content.decode('utf-8').lower()
        for term in terms:
            res = cleaned.find(term.lower())
            if res >= 0:
                IPOStringModel.update_string_as_found(term)
                self.info("Company IPO announced: " + term)

    def add_string(self, string):
        IPOStringModel.insert_string_if_not_exists(string)

    def remove_string(self, string):
        IPOStringModel.remove_string_if_not_found(string)

    def dismiss_string(self, string):
        IPOStringModel.update_string_as_dismissed(string)

    def get_data(self):
        res = IPOStringModel.get_all_not_dismissed_strings()
        return {'res': res, 'sites': self.SITES}

    def execute(self, command, **kwargs):
        string = kwargs['string']
        if command == 'add':
            self.add_string(string)
        elif command == 'remove':
            self.remove_string(string)
        elif command == 'dismiss':
            self.dismiss_string(string)
