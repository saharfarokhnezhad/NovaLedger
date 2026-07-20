from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


class SettingsScreen(MDScreen):

    def logout(self):
        app = MDApp.get_running_app()
        app.current_user = None
        app.root.current = "login"

    def change_theme(self, active):
        app = MDApp.get_running_app()

        if active:
            app.theme_cls.theme_style = "Dark"
        else:
            app.theme_cls.theme_style = "Light"