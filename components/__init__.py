from kivymd.uix.navigationdrawer import MDNavigationDrawer

class SideBar(MDNavigationDrawer):
    def set_user_data(self, user_data):
        self.ids.avatar.source = user_data['user']['avatar']
        self.ids.username.text = user_data['user']['name']
            

