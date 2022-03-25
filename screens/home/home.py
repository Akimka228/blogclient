import json
from turtle import home
from kivymd.toast import toast
from kivymd.app import MDApp
from kivy.network.urlrequest import UrlRequest
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCardSwipeFrontBox, MDCardSwipe
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import ThreeLineAvatarListItem, ImageLeftWidget, IconRightWidget, ImageRightWidget, \
    ThreeLineAvatarIconListItem
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.textfield import MDTextField
from kivy.properties import NumericProperty, StringProperty
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.card import MDCardSwipeFrontBox, MDCardSwipe, MDCard
from kivy.animation import Animation
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior


import components


class HomeScreen(Screen):
    dialog = None
    current_user_id = None
    current_username = None

    def on_pre_enter(self):
        self.load_posts()
        storage = JsonStore('cache.json')
        self.current_username = storage.get('user')['name']
        self.current_user_id = storage.get('user')['id']

    def show_posts(self, *args):
        posts = json.loads(args[1])
        scroll_list = self.ids.posts
        scroll_list.clear_widgets()
        for post in posts:
            post_ = Post(id=post['id'],
                         author_name=post['author']['username'],
                         author_id=post['author']['id'],
                         text=post['text'],
                         likes_count = str(post['likes_count']),
                         avatar=post['author']['avatar'],
                         )
            scroll_list.add_widget(post_)

    def load_posts(self):
        UrlRequest(f'http://localhost:5000/api/posts',
                   on_success=self.show_posts)

    def on_success_posting(self, *args):
        toast('Post added!')
        self.load_posts()

    def send_post(self, *args):
        text_post = self.dialog.content_cls.text
        r = UrlRequest(
            f'http://localhost:5000/api/add_post?post_text={text_post}&username={self.current_username}', on_success=self.on_success_posting)
        self.close_dialog()

    def close_dialog(self, *args):
        self.dialog.dismiss()

    def open_dialog(self):
        self.dialog = MDDialog(
            title='Add post',
            type='custom',
            content_cls=MDTextField(
                multiline=True,
                pos_hint={'center_y': 0.2},
                max_height="110dp"
            ),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    # text_color=app.theme_cls.primary_color,
                    on_release=self.close_dialog
                ),
                MDFlatButton(
                    text="Send",
                    theme_text_color="Custom",
                    # text_color=app.theme_cls.primary_color,
                    on_release=self.send_post
                ),
            ],
        )

        self.dialog.open()


class Post(MDCard, RoundedRectangularElevationBehavior):
    id = NumericProperty()
    text = StringProperty()
    author_name = StringProperty()
    author_id = NumericProperty()
    avatar = StringProperty()
    likes_count = StringProperty()

    def show_full_post(self):
        dialog = MDDialog(
            title="Post",
            text=f"[color=#000]{self.tertiary_text}[/color]"
        )
        dialog.open()

    def delete_post_animate(self):
        anim = Animation(x=1000, duration=0.2)
        anim.bind(on_complete=self.delete_post)
        anim.start(self)

    def delete_post(self, *args):
        home_screen = MDApp.get_running_app().root.get_screen('home')
        home_screen.ids.posts.remove_widget(self)
        r = UrlRequest(
            f'http://localhost:5000/api/delete_post?post_id={self.id}&user_id={home_screen.current_user_id}', on_success=self.success_deleting)

    def success_deleting(self, *args):
        toast('Post Deleted!')

    def open_profile(self, user_id):
        profile_screen = MDApp.get_running_app().root.get_screen('profile')
        profile_screen.profile_user_id = user_id
        MDApp.get_running_app().root.current = 'profile'
    
    def like_post(self):
        home_screen = MDApp.get_running_app().root.get_screen('home')
        r = UrlRequest(
            f'http://localhost:5000/api/set_like?post_id={self.id}&user_id={home_screen.current_user_id}',on_success=self.increase_likes_count)

    def increase_likes_count(self, *args):
        current_post_likes_count = args[1]
        self.ids.likes_count.text = current_post_likes_count
