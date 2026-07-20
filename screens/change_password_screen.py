from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


class ChangePasswordScreen(MDScreen):

    def change_password(self):

        app = MDApp.get_running_app()

        old_password = self.ids.old_password.text.strip()
        new_password = self.ids.new_password.text.strip()
        confirm_password = self.ids.confirm_password.text.strip()

        if old_password == "" or new_password == "" or confirm_password == "":
            return

        if not app.db.check_current_password(
            app.current_user["id"],
            old_password
):
            return

        if new_password != confirm_password:
            return

        app.db.cursor.execute(
            """
            UPDATE users
            SET password = ?
            WHERE id = ?
            """,
            (
                new_password,
                app.current_user["id"]
            )
        )

        app.db.connection.commit()

        self.ids.old_password.text = ""
        self.ids.new_password.text = ""
        self.ids.confirm_password.text = ""

        app.root.current = "settings"