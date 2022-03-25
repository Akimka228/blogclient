from kivy.lang import Builder
from kivymd.app import MDApp
from screens.login import login
from screens.register import register
from screens.home import home
from screens.profile import profile



class MainApp(MDApp):
    user_data = {"id": 7, "name": "Vasya", "avatar": "https://gravatar.com/avatar/d1ac1d1dea13f23105217c5d0bc69b5f?d=identicon&s=256"}
    def build(self):
        self.load_kv('screens/login/login.kv')
        self.load_kv('screens/register/register.kv')
        self.load_kv('screens/home/home.kv')
        self.load_kv('screens/profile/profile.kv')
        return Builder.load_file('main.kv')

    
    def switch_screen(self, screen_name):
        self.root.current = screen_name

    def on_start(self):
        self.sm = self.root

MainApp().run()
