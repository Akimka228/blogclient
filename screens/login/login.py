import json
from kivymd.app import MDApp
from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty
from kivymd.toast import toast
from kivy.uix.screenmanager import Screen
from kivy.storage.jsonstore import JsonStore


class LoginScreen(Screen):
    def login(self):
        username = self.ids["username"].text
        password = self.ids["password"].text
        UrlRequest(f'http://localhost:5000/api/login?username={username}&password={password}',
                   on_failure=self.on_login_fail, on_success=self.success_login)

    def on_login_fail(self, *args):
        toast('Invalid username/password')

    def success_login(self, *args):
        current_app = MDApp.get_running_app()
        storage = JsonStore('cache.json')
        user_data = json.loads(args[1])
        storage.put('user', id=user_data['user']['id'], name=user_data['user']
                    ['name'], avatar=user_data['user']['avatar'])
        current_app.root.current = 'home'
        current_app.user_data = user_data['user']
        current_app.root.get_screen('home').ids.sidebar.set_user_data(user_data)

