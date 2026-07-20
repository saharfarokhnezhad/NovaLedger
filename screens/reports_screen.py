from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
import matplotlib.pyplot as plt
from kivy.core.image import Image as CoreImage
from io import BytesIO
from kivymd.uix.pickers import MDModalDatePicker


class ReportsScreen(MDScreen):

    start_date = None
    end_date = None
    
    def on_pre_enter(self):
        super().on_pre_enter()
        self.load_report()

    def load_report(self):

        app = MDApp.get_running_app()

        user_id = app.current_user["id"]

        income = app.db.get_total_income(user_id)
        expense = app.db.get_total_expense(user_id)
        balance = income - expense
        transactions = app.db.get_transaction_count(user_id)

        self.ids.income_label.text = f"{income:,.0f}"
        self.ids.expense_label.text = f"{expense:,.0f}"
        self.ids.balance_label.text = f"{balance:,.0f}"
        self.ids.transaction_label.text = str(transactions)
        self.load_pie_chart()
        self.load_line_chart()

    def load_pie_chart(self):

        app = MDApp.get_running_app()

        data = app.db.get_expense_by_category(
            app.current_user["id"]
        )

        if not data:
            return

        labels = [row[0] for row in data]
        values = [row[1] for row in data]

        plt.clf()

        plt.pie(
            values,
            labels=labels,
            autopct="%1.0f%%",
            startangle=90
        )
        plt.axis("equal")

        buffer = BytesIO()

        plt.savefig(
            buffer,
            format="png",
            bbox_inches="tight"
        )

        buffer.seek(0)

        image = CoreImage(buffer, ext="png")

        self.ids.pie_chart.texture = image.texture

        plt.close()

    def load_line_chart(self):

        app = MDApp.get_running_app()

        income = dict(
            app.db.get_monthly_income(app.current_user["id"])
        )

        expense = dict(
            app.db.get_monthly_expense(app.current_user["id"])
        )

        months = sorted(
            set(income.keys()) | set(expense.keys())
        )

        income_values = [
            income.get(month, 0)
            for month in months
        ]

        expense_values = [
            expense.get(month, 0)
            for month in months
        ]

        plt.clf()

        plt.figure(figsize=(5,3))
        plt.style.use("ggplot")

        plt.plot(
            months,
            income_values,
            marker="o",
            label="Income"
        )

        plt.plot(
            months,
            expense_values,
            marker="o",
            label="Expense"
        )

        plt.legend(loc="upper left")

        plt.grid(True)
        plt.xticks(rotation=30)
        plt.tight_layout()

        buffer = BytesIO()

        plt.savefig(
            buffer,
            format="png",
            bbox_inches="tight"
        )

        buffer.seek(0)

        image = CoreImage(buffer, ext="png")

        self.ids.line_chart.texture = image.texture

        plt.close()

    def open_date_picker(self):

        picker = MDModalDatePicker()

        picker.bind(on_ok=self.set_report_date)

        picker.open()

    def on_date_selected(self, picker):

        dates = picker.get_date()

        if len(dates) == 2:

            self.start_date = str(dates[0])
            self.end_date = str(dates[1])

            self.load_report()

        picker.dismiss()


    def set_report_date(self, picker):

        selected = picker.get_date()[0]

        self.ids.date_button.children[0].text = selected.strftime("%Y-%m")

        picker.dismiss()




    