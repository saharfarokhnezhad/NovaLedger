import os
import sys
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screenmanager import MDScreenManager

from database.database import Database

from screens.splash_screen import SplashScreen
from screens.login_screen import LoginScreen
from screens.register_screen import RegisterScreen
from screens.dashboard_screen import DashboardScreen
from screens.add_expense_screen import AddExpenseScreen
from screens.add_income_screen import AddIncomeScreen
from screens.categories_screen import CategoriesScreen
from screens.reports_screen import ReportsScreen
from screens.settings_screen import SettingsScreen
from screens.profile_screen import ProfileScreen
from screens.change_password_screen import ChangePasswordScreen
from screens.about_screen import AboutScreen
from screens.reports_screen import ReportsScreen
from kivy.core.window import Window
from screens.edit_transaction_screen import EditTransactionScreen

Window.size = (360, 640)


class ExpenseManagerApp(MDApp):

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def build(self):

        self.title = "NovaLedger"

        # Theme
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "600"

        # Load KV Files
        Builder.load_file(self.resource_path("splash.kv"))
        Builder.load_file(self.resource_path("login.kv"))
        Builder.load_file(self.resource_path("register.kv"))
        Builder.load_file(self.resource_path("dashboard.kv"))
        Builder.load_file(self.resource_path("add_income_screen.kv"))
        Builder.load_file(self.resource_path("add_expense_screen.kv"))
        Builder.load_file(self.resource_path("categories.kv"))
        Builder.load_file(self.resource_path("setting.kv"))
        Builder.load_file(self.resource_path("profile.kv"))
        Builder.load_file(self.resource_path("change_password.kv"))
        Builder.load_file(self.resource_path("about.kv"))
        Builder.load_file(self.resource_path("reports.kv"))
        Builder.load_file(self.resource_path("edit_transaction.kv"))
    
        self.db = Database()
        self.current_user = None
        self.edit_transaction_id = None

        sm = MDScreenManager()

        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(AddExpenseScreen(name="add_expense"))
        sm.add_widget(AddIncomeScreen(name="add_income"))
        sm.add_widget(CategoriesScreen(name="categories"))
        sm.add_widget(ReportsScreen(name="reports"))
        sm.add_widget(SettingsScreen(name="settings"))
        sm.add_widget(ProfileScreen(name="profile"))
        sm.add_widget(ChangePasswordScreen(name="change_password"))
        sm.add_widget(AboutScreen(name="about"))
        sm.add_widget(EditTransactionScreen(name="edit_transaction"))

        return sm


ExpenseManagerApp().run()