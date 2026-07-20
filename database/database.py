import sqlite3



class Database:

    def __init__(self):
        self.connection = sqlite3.connect("expense.db")
        self.cursor = self.connection.cursor()

        self.create_tables()

    def create_tables(self):

        # Users Table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                created_at TEXT
            )
        """)

        # Categories Table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                type TEXT NOT NULL,

                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)

        # Transactions Table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,

                category_id INTEGER NOT NULL,

                title TEXT NOT NULL,

                type TEXT NOT NULL,

                amount REAL NOT NULL,

                description TEXT,

                date TEXT NOT NULL,

            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(category_id) REFERENCES categories(id)

        )
        """)

        self.connection.commit()

    # ---------------- USERS ---------------- #

    def add_user(self, username, password):
        self.cursor.execute(
            """
            INSERT INTO users (username, password)
            VALUES (?, ?)
            """,
            (username, password)
        )

        self.connection.commit()

    def get_user(self, username):
        self.cursor.execute(
            """
            SELECT * FROM users
            WHERE username = ?
            """,
            (username,)
        )

        return self.cursor.fetchone()

    def get_user_by_id(self, user_id):
        self.cursor.execute(
            """
            SELECT * FROM users
            WHERE id = ?
            """,
            (user_id,)
        )

        return self.cursor.fetchone()

    def check_login(self, username, password):
        self.cursor.execute(
            """
            SELECT * FROM users
            WHERE username = ? AND password = ?
            """,
            (username, password)
        )

        return self.cursor.fetchone()

    # ---------------- CATEGORIES ---------------- #

    def add_category(self, user_id, name, category_type):
        self.cursor.execute(
            """
            INSERT INTO categories (user_id, name, type)
            VALUES (?, ?, ?)
            """,
            (user_id, name, category_type)
        )

        self.connection.commit()

    # ---------------- TRANSACTIONS ---------------- #

    def add_transaction(
        self,
        user_id,
        category_id,
        title,
        type_,
        amount,
        description,
        date
    ):

        self.cursor.execute(
            """
            INSERT INTO transactions
            (
                user_id,
                category_id,
                title,
                type,
                amount,
                description,
                date
            )

            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                category_id,
                title,
                type_,
                amount,
                description,
                date
            )
        )
        self.connection.commit()


    def create_default_categories(self, user_id):

        income = [
            "Salary",
            "Freelance",
            "Investment",
            "Gift"
        ]

        expense = [
            "Food",
            "Coffee",
            "Transport",
            "Shopping",
            "Entertainment",
            "Bills",
            "Health",
            "Education"
        ]

        for category in income:
            self.add_category(user_id, category, "income")

        for category in expense:
            self.add_category(user_id, category, "expense")

    def get_categories(self, user_id, type_):

        self.cursor.execute(
            """
            SELECT id, name
            FROM categories

            WHERE user_id = ?
            AND type = ?
            """,
            (
                user_id,
                type_
            )
        )

        return self.cursor.fetchall()
    
    def get_total_income(self, user_id):

        self.cursor.execute(
            """
            SELECT SUM(amount)
            FROM transactions
            WHERE user_id = ?
            AND type = 'income'
            """,
            (user_id,)
        )

        result = self.cursor.fetchone()[0]

        return result if result else 0


    def get_total_expense(self, user_id):

        self.cursor.execute(
            """
            SELECT SUM(amount)
            FROM transactions
            WHERE user_id = ?
            AND type = 'expense'
            """,
            (user_id,)
        )

        result = self.cursor.fetchone()[0]

        return result if result else 0
    
    def get_recent_transactions(self, user_id):

        self.cursor.execute("""
            SELECT
                transactions.id,
                categories.name,
                transactions.title,
                transactions.amount,
                transactions.type,
                transactions.date

            FROM transactions

            JOIN categories
            ON transactions.category_id = categories.id

            WHERE transactions.user_id = ?

            ORDER BY transactions.id DESC

            LIMIT 20
            """, (user_id,))

        return self.cursor.fetchall()
    
    def search_transactions(self, user_id, keyword):

        self.cursor.execute("""
            SELECT
                transactions.id,
                categories.name,
                transactions.title,
                transactions.amount,
                transactions.type,
                transactions.date

            FROM transactions

            JOIN categories
            ON transactions.category_id = categories.id

            WHERE transactions.user_id = ?

            AND (
                transactions.title LIKE ?
                OR categories.name LIKE ?
            )

            ORDER BY transactions.id DESC
            """, (
            user_id,
            f"%{keyword}%",
            f"%{keyword}%"
            ))

        return self.cursor.fetchall()
    
    def get_transaction_count(self, user_id):

        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM transactions
            WHERE user_id = ?
            """,
            (user_id,)
        )

        return self.cursor.fetchone()[0]
    
    def check_current_password(self, user_id, password):

        self.cursor.execute(
            """
            SELECT id
            FROM users
            WHERE id = ? AND password = ?
            """,
            (user_id, password)
        )

        return self.cursor.fetchone() is not None

    def delete_transaction(self, transaction_id):

        self.cursor.execute("""
            DELETE FROM transactions
            WHERE id = ?
            """, (transaction_id,))

        self.connection.commit()

    def get_transaction(self, transaction_id):
        self.cursor.execute("""
        SELECT
            id,
            user_id,
            category_id,
            title,
            type,
            amount,
            description,
            date
        FROM transactions
        WHERE id = ?
        """, (transaction_id,))

        return self.cursor.fetchone()
    
    def update_transaction(
        self,
        transaction_id,
        category_id,
        title,
        amount,
        description,
        date
):

        self.cursor.execute("""
            UPDATE transactions

            SET

            category_id = ?,
            title = ?,
            amount = ?,
            description = ?,
            date = ?

            WHERE id = ?
            """, (

            category_id,
            title,
            amount,
            description,
            date,
            transaction_id

        ))

        self.connection.commit()

    def get_report_data(self, user_id):

        income = self.get_total_income(user_id)
        expense = self.get_total_expense(user_id)
        balance = income - expense
        transactions = self.get_transaction_count(user_id)

        return {
            "income": income,
            "expense": expense,
            "balance": balance,
            "transactions": transactions
        }
    
    def get_expense_by_category(self, user_id):

        self.cursor.execute("""
            SELECT
                categories.name,
                SUM(transactions.amount)

            FROM transactions

            JOIN categories
            ON transactions.category_id = categories.id

            WHERE
                transactions.user_id = ?
                AND transactions.type = 'expense'

            GROUP BY categories.name

            ORDER BY SUM(transactions.amount) DESC
            """, (user_id,))

        return self.cursor.fetchall()
    
    def get_monthly_income(self, user_id):

        self.cursor.execute("""
            SELECT
                substr(date, 1, 7),
                SUM(amount)

            FROM transactions

            WHERE
                user_id = ?
                AND type='income'

            GROUP BY substr(date,1,7)

            ORDER BY substr(date,1,7)
            """, (user_id,))

        return self.cursor.fetchall()
    
    def get_monthly_expense(self, user_id):

        self.cursor.execute("""
            SELECT
                substr(date,1,7),
                SUM(amount)

            FROM transactions

            WHERE
                user_id = ?
                AND type='expense'

            GROUP BY substr(date,1,7)

            ORDER BY substr(date,1,7)
            """, (user_id,))

        return self.cursor.fetchall()

    def close(self):
        self.connection.close()