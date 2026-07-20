from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.uix.screenmanager import FadeTransition


class SplashScreen(MDScreen):

    def on_enter(self):
        Clock.unschedule(self.goto_login)
        Clock.schedule_once(self.goto_login, 5)

    def goto_login(self, *args):
        self.manager.transition = FadeTransition(duration=0.5)
        self.manager.current = "login"