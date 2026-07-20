from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu


class EditTransactionScreen(MDScreen):

    def on_pre_enter(self):

        app = MDApp.get_running_app()

        self.transaction = app.db.get_transaction(
            app.edit_transaction_id
        )

        (
            self.transaction_id,
            user_id,
            category_id,
            title,
            trans_type,
            amount,
            description,
            date
        ) = self.transaction

        self.transaction_type = trans_type
        self.selected_category = category_id

        self.ids.title_field.text = title
        self.ids.amount_field.text = str(amount)
        self.ids.description_field.text = description if description else ""
        self.ids.date_field.text = date

        self.load_categories()


    def load_categories(self):

        app = MDApp.get_running_app()

        categories = app.db.get_categories(
            app.current_user["id"],
            self.transaction_type
        )

        self.menu_items = []

        for category_id, name in categories:

            self.menu_items.append({

                "text": name,

                "on_release": lambda cid=category_id, n=name:
                    self.select_category(cid, n)

            })

        for cid, name in categories:
            if cid == self.selected_category:
                self.ids.category_item.text = name
                break


    def open_category_menu(self):

        self.menu = MDDropdownMenu(

            caller=self.ids.category_item,

            items=self.menu_items,

            width=4

        )

        self.menu.open()


    def select_category(self, category_id, name):

        self.selected_category = category_id

        self.ids.category_item.text = name

        self.menu.dismiss()


    def save_changes(self):

        app = MDApp.get_running_app()

        app.db.update_transaction(

            self.transaction_id,
            self.selected_category,
            self.ids.title_field.text,
            float(self.ids.amount_field.text),
            self.ids.description_field.text,
            self.ids.date_field.text

        )

        dashboard = app.root.get_screen("dashboard")
        dashboard.load_data()

        app.root.current = "dashboard"


    def delete_transaction(self):

        app = MDApp.get_running_app()

        app.db.delete_transaction(
            self.transaction_id
        )

        dashboard = app.root.get_screen("dashboard")
        dashboard.load_data()

        app.root.current = "dashboard"