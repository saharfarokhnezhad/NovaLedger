from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp


class RegisterScreen(MDScreen):

    def register(self):

        app = MDApp.get_running_app()

        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()
        confirm = self.ids.confirm_password.text.strip()

        # فیلدهای خالی
        if not username or not password or not confirm:
            print("Fill all fields")
            return

        # یکی بودن رمزها
        if password != confirm:
            print("Passwords do not match")
            return

        # تکراری نبودن نام کاربری
        if app.db.get_user(username):
            print("Username already exists")
            return

        # ثبت در دیتابیس
        app.db.add_user(username, password)

        print("Registration successful")

        self.manager.current = "login"

        user = app.db.get_user(username)
        app.db.create_default_categories(user[0])

    def go_login(self):
        self.manager.current = "login"