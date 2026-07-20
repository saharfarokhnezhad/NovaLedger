from kivymd.app import MDApp
from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemSupportingText
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDButton, MDButtonText
from kivy.clock import Clock
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.snackbar import MDSnackbarActionButton
from kivymd.uix.snackbar import MDSnackbarActionButtonText
from kivymd.uix.snackbar import MDSnackbarText
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel


class DashboardScreen(MDScreen):

    def on_pre_enter(self):
        self.load_data()

    def load_data(self):

        app = MDApp.get_running_app()

        if app.current_user is None:
            return

        user_id = app.current_user["id"]

        income = app.db.get_total_income(user_id)
        expense = app.db.get_total_expense(user_id)

        balance = income - expense

        self.ids.balance_label.text = f"{balance:,.0f}"
        self.ids.income_label.text = f"{income:,.0f}"
        self.ids.expense_label.text = f"{expense:,.0f}"

        self.load_transactions()

    def load_transactions(self):

        app = MDApp.get_running_app()

        self.ids.transactions_container.clear_widgets()

        transactions = app.db.get_recent_transactions(
            app.current_user["id"]
        )

        for trans_id, category, title, amount, trans_type, date in transactions:

            sign = "+" if trans_type == "income" else "-"
            amount_color = "#0BB229" if trans_type == "income" else "#EF5350"

            card = MDCard(
                style="elevated",
                radius=[18],
                size_hint_y=None,
                height="90dp",
                padding="12dp",
                ripple_behavior=True,
            )

            row = MDBoxLayout(
                orientation="horizontal",
                spacing="10dp"
            )

            left = MDBoxLayout(
                orientation="vertical",
                size_hint_x=.75,
                spacing="3dp",
            )

            title_label = MDLabel(
                text=title,
                bold=True,
                font_style="Title",
                adaptive_height=True,
            )

            info_label = MDLabel(
                text=f"{category} • {date}",
                theme_text_color="Secondary",
                adaptive_height=True,
            )

            amount_label = MDLabel(
                text=f"{sign}{amount:,.0f}",
                size_hint_x=.25,
                halign="right",
                valign="middle",
                theme_text_color="Custom",
                text_color=amount_color,
                bold=True,
            )

        # این خط خیلی مهمه
            amount_label.bind(size=amount_label.setter("text_size"))

            left.add_widget(title_label)
            left.add_widget(info_label)

            row.add_widget(left)
            row.add_widget(amount_label)

            card.add_widget(row)

            card.bind(
                on_release=lambda x, tid=trans_id:
                self.open_transaction_menu(tid)
            )

            self.ids.transactions_container.add_widget(card)

    def open_add_menu(self):

        menu_items = [

            {
                "text": " Add Income",
                "on_release": lambda: self.open_income()
            },

            {
                "text": " Add Expense",
                "on_release": lambda: self.open_expense()
            }

        ]

        self.menu = MDDropdownMenu(
            caller=self.ids.add_button,
            items=menu_items,
            width=4
        )

        self.menu.open()


    def open_income(self):

        self.menu.dismiss()
        MDApp.get_running_app().root.current = "add_income"


    def open_expense(self):

        self.menu.dismiss()
        MDApp.get_running_app().root.current = "add_expense"


    def change_screen(self, screen_name):

        self.menu.dismiss()

        MDApp.get_running_app().root.current = screen_name

    def open_transaction_menu(self, transaction_id):

        self.selected_transaction = transaction_id

        items = [

            {
                "text": "Edit",
                "on_release": lambda: self.edit_transaction()
            },

            {
                "text": "Delete",
                "on_release": lambda: self.delete_transaction()
            }

        ]

        self.transaction_menu = MDDropdownMenu(
            caller=self,
            items=items,
            width=4,
        )

        self.transaction_menu.open()

    def delete_transaction(self):

        app = MDApp.get_running_app()

        self.deleted_transaction = app.db.get_transaction(
            self.selected_transaction
        )

        app.db.delete_transaction(self.selected_transaction)

        self.load_data()

        snackbar = MDSnackbar(
            MDSnackbarActionButton(
                MDSnackbarActionButtonText(
                    text="UNDO"
                ),
                on_release=lambda x: self.undo_delete()
            ),
            duration=10,
        )

        snackbar.add_widget(
            MDSnackbarText(
                text="Transaction deleted"
            )
        )

        snackbar.open()

        self.delete_event = Clock.schedule_once(
            self.clear_deleted_transaction,
            10
        )

    def edit_transaction(self):

        app = MDApp.get_running_app()

        app.edit_transaction_id = self.selected_transaction

        if hasattr(self, "transaction_menu"):
            self.transaction_menu.dismiss()

        app.root.current = "edit_transaction"

    def undo_delete(self):

        if not self.deleted_transaction:
            return

        app = MDApp.get_running_app()

        (
            _id,
            user_id,
            category_id,
            title,
            trans_type,
            amount,
            description,
            date
        ) = self.deleted_transaction

        app.db.add_transaction(
            user_id,
            category_id,
            title,
            trans_type,
            amount,
            description,
            date
        )

        self.delete_event.cancel()

        self.deleted_transaction = None

        self.load_data()


    def clear_deleted_transaction(self, dt):

        self.deleted_transaction = None

    def search_transactions(self, keyword):

        app = MDApp.get_running_app()

        self.ids.transactions_container.clear_widgets()

        if keyword.strip() == "":
            self.load_transactions()
            return

        transactions = app.db.search_transactions(
            app.current_user["id"],
            keyword
        )

        for trans_id, category, title, amount, trans_type, date in transactions:

            sign = "+" if trans_type == "income" else "-"
            amount_color = "#0BB229" if trans_type == "income" else "#EF5350"

            card = MDCard(
                style="elevated",
                radius=[18],
                size_hint_y=None,
                height="90dp",
                padding="12dp",
                ripple_behavior=True,
            )

            row = MDBoxLayout(
                orientation="horizontal",
                spacing="10dp"
            )

            left = MDBoxLayout(
                orientation="vertical",
                size_hint_x=.75,
                spacing="3dp",
            )

            title_label = MDLabel(
                text=title,
                bold=True,
                font_style="Title",
                adaptive_height=True,
            )

            info_label = MDLabel(
                text=f"{category} • {date}",
                theme_text_color="Secondary",
                adaptive_height=True,
            )

            amount_label = MDLabel(
                text=f"{sign}{amount:,.0f}",
                size_hint_x=.25,
                halign="right",
                valign="middle",
                theme_text_color="Custom",
                text_color=amount_color,
                bold=True,
            )

            amount_label.bind(size=amount_label.setter("text_size"))

            left.add_widget(title_label)
            left.add_widget(info_label)

            row.add_widget(left)
            row.add_widget(amount_label)

            card.add_widget(row)

            card.bind(
                on_release=lambda x, tid=trans_id: self.open_transaction_menu(tid)
            )

            self.ids.transactions_container.add_widget(card)