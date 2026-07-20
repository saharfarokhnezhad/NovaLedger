from datetime import datetime

from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivymd.uix.pickers import MDModalDatePicker


class AddIncomeScreen(MDScreen):

    selected_category = None

    def open_categories(self):

        app = MDApp.get_running_app()

        categories = app.db.get_categories(
            app.current_user["id"],
            "income"
        )

        items = []

        for category in categories:

            items.append(
                {
                    "text": category[1],
                    "on_release": lambda x=category: self.select_category(x)
                }
            )

        self.menu = MDDropdownMenu(
            caller=self.ids.category_field,
            items=items,
            width=4
        )

        self.menu.open()

    def select_category(self, category):

        self.selected_category = category[0]

        self.ids.category_field.text = category[1]

        self.menu.dismiss()

    def save_income(self):

        app = MDApp.get_running_app()

        title = self.ids.title_field.text
        amount = self.ids.amount_field.text
        description = self.ids.description_field.text

        if amount == "":
            return

        if self.selected_category is None:
            return
        
        if self.ids.date_field.text == "":
            self.ids.date_field.text = datetime.now().strftime("%Y-%m-%d")
        app.db.add_transaction(
            user_id=app.current_user["id"],
            category_id=self.selected_category,
            title=title,
            type_="income",
            amount=float(amount),
            description=description if description else title,
            date=self.ids.date_field.text
        )

        self.ids.title_field.text = ""
        self.ids.amount_field.text = ""
        self.ids.description_field.text = ""
        self.ids.category_field.text = ""
        self.ids.date_field.text = ""

        self.selected_category = None

        app.root.current = "dashboard"
        

    def open_date_picker(self):

        picker = MDModalDatePicker()
        picker.bind(on_ok=self.set_date)
        picker.open()


    def set_date(self, picker):

        self.ids.date_field.text = str(picker.get_date()[0])
        picker.dismiss()