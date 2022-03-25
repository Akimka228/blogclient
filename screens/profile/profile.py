import json

from kivy.animation import Animation
from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from screens.home.home import Post

from kivymd.uix.toolbar import MDToolbar

class ProfileScreen(Screen):
    profile_user_id = NumericProperty()
    profile_username = StringProperty()
    

    def on_pre_enter(self):
        UrlRequest(f'http://127.0.0.1:5000/api/get_user?id={self.profile_user_id}', on_success=self.on_user_data_load)

    def on_user_data_load(self, *args):
        user_data = json.loads(args[1])
        self.ids.avatar_bg.source = user_data['avatar_source']
        self.ids.rounded_avatar.source = user_data['avatar_source']
        self.ids.username.text = user_data['username']
        
        ### SHOW POSTS ###
        posts = user_data['posts']
        scroll_list = self.ids.posts
        scroll_list.clear_widgets()
        for post in posts:
            post_ = Post(id=post['post_id'],
                         author_name=user_data['username'],
                         author_id=user_data['id'],
                         text=post['text'],
                         avatar=user_data['avatar_source']
                         )
            scroll_list.add_widget(post_)


class MyToolBar(MDToolbar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type_height = 'medium'
        self.left_action_items = [['arrow-left', lambda x: MDApp.get_running_app().switch_screen('home')]]