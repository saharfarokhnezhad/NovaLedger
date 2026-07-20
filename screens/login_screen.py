from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp


class LoginScreen(MDScreen):

    def login(self):

        app = MDApp.get_running_app()

        username = self.ids.username_field.text.strip()
        password = self.ids.password_field.text.strip()

        if not username or not password:
            print("Please fill all fields")
            return

        user = app.db.check_login(username, password)

        if user:
            print("Login Successful")

            app.current_user = {
                "id": user[0],
                "username": user[1]
            }

            self.manager.current = "dashboard"

        else:
            print("Invalid username or password")

    def go_register(self):
        self.manager.current = "register"