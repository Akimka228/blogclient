from kivy.factory import Factory
from kivy.core.window import Window
from kaki.app import App
from kivymd.app import MDApp
import os


class HotReload(App, MDApp):
    CLASSES = {
        'Main': 'main'
    }
    AUTORELOADER_PATHS = [
        ('.', {'recursive': True})
    ]
    KV_FILES = {
        os.path.join(os.getcwd(), 'main.kv')
    }

    def build_app(self):
        return Factory.Main()


if __name__ == '__main__':
    HotReload().run()


# set DEBUG=1 && python live.py