from common.cache import hash_tuple
from common.enums import APP, APPSTATUS
from database.config.apps_model import AppsModel


class AppManager:

    IS_RUNNING = False

    def __init__(self):

        if self.IS_RUNNING:
            raise Exception('Only one instance of AppManager allowed')

        self.IS_RUNNING = True
        self.apps_model = AppsModel()
        # Import all running apps
        from apps.online_apps import APPS
        self.apps = APPS

    def get_all_apps(self):
        res = self.apps_model.get_all_online_apps()
        for key, value in res.items():
            app_entry = res[key]
            app_entry['status'] = APPSTATUS.UNKNOWN.value
            try:
                app = APP(key)
                if app in self.apps:
                    app_entry['status'] = self.apps[app].status.value
            except ValueError:
                if 'https' in app_entry['url']:
                    app_entry['status'] = APPSTATUS.LINK.value
        return res

    def get_app_status(self, app_id):
        app = self.apps[APP(app_id)]
        base_data = {'status': app.status.value, 'debugging': app.debugging}
        additional_data = app.get_data()
        return {**base_data, **additional_data}

    def get(self, app_id, command):
        app = self.apps[APP(app_id)]
        res = app.get(command)
        return res

    def blob(self, app_id, command):
        app = self.apps[APP(app_id)]
        file_path = app.blob(command)
        return file_path

    def execute(self, app_id, command, data=None):
        app = self.apps[APP(app_id)]

        # Pre-defined routines
        if command == 'run':
            app.run(**data)
            return {}
        elif command == 'debug':
            app.debugging = data['isDebug']
            return {}
        elif command == 'get':
            return app.get_data()

        # Arbitrary commands

        # Return results if it's found in cache
        hash_id = hash_tuple((command, data))

        res = app.try_cache(hash_id)
        if res is not None:
            return res

        # Execute commands and put in cache
        if data is None:
            res = app.execute(command, **{})
        else:
            res = app.execute(command, **data)

        app.store_to_cache(command, data, res)
        return res
