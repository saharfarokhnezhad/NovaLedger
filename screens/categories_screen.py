from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDListItem, MDListItemHeadlineText


class CategoriesScreen(MDScreen):

    def on_pre_enter(self):
        self.load_categories()

    def add_category(self):

        app = MDApp.get_running_app()

        name = self.ids.category_name.text.strip()

        if name == "":
            return

        if self.ids.income_btn.active:
            category_type = "income"
        else:
            category_type = "expense"

        app.db.add_category(
            app.current_user["id"],
            name,
            category_type
        )

        self.ids.category_name.text = ""

        self.load_categories()

    def load_categories(self):

        app = MDApp.get_running_app()

        self.ids.categories_list.clear_widgets()

        income = app.db.get_categories(
            app.current_user["id"],
            "income"
        )

        expense = app.db.get_categories(
            app.current_user["id"],
            "expense"
        )

        for category in income:

            self.ids.categories_list.add_widget(

                MDListItem(

                    MDListItemHeadlineText(
                        text=f" {category[1]}"
                    )

                )

            )

        for category in expense:

            self.ids.categories_list.add_widget(

                MDListItem(

                    MDListItemHeadlineText(
                        text=f" {category[1]}"
                    )

                )

            )