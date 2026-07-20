from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


class ProfileScreen(MDScreen):

    def on_pre_enter(self):
        self.load_profile()

    def load_profile(self):

        app = MDApp.get_running_app()

        user = app.current_user

        self.ids.username_label.text = user["username"]

        income = app.db.get_total_income(user["id"])
        expense = app.db.get_total_expense(user["id"])

        balance = income - expense

        self.ids.income_label.text = f"{income:,.0f}"
        self.ids.expense_label.text = f"{expense:,.0f}"
        self.ids.balance_label.text = f"{balance:,.0f}"
        
        count = app.db.get_transaction_count(user["id"])
        self.ids.transaction_count.text = str(count)