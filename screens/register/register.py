from kivy.network.urlrequest import UrlRequest
from kivymd.app import MDApp
from kivymd.toast import toast
from kivy.uix.screenmanager import Screen
class RegisterScreen(Screen):
    def register(self):        
        username = self.ids["username"].text
        password = self.ids["password"].text
        email = self.ids["email"].text
        UrlRequest(f'http://localhost:5000/api/register?username={username}&password={password}&email={email}', on_failure=self.on_register_fail, on_success=self.on_success_register)

    def on_register_fail(self, *args):
        toast('User already exist')
    
    def on_success_register(self, *args):
        toast('Success!')
        self.root.current = 'login'
