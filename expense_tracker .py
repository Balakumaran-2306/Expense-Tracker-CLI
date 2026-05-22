import os
import csv
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import getpass

DB_NAME = "expense_tracker.db"


# ================= DATABASE =================

def init_db():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        time TEXT,
        type TEXT,
        amount REAL,
        detail TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


# ================= COMMON =================

def get_current_datetime():

    now = datetime.now()

    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    return date, time


def menu():

    print("\n========== 💰 Expense Tracker ==========")

    print("1️⃣ Add Income")
    print("2️⃣ Add Expense")
    print("3️⃣ View Transactions")
    print("4️⃣ View Balance")
    print("5️⃣ Search Transactions")
    print("6️⃣ Delete Transaction")
    print("7️⃣ Update Transaction")
    print("8️⃣ Monthly Report")
    print("9️⃣ Budget Check")
    print("🔟 Show Expense Chart")
    print("11️⃣ Export CSV")
    print("12️⃣ Logout")
    print("13️⃣ Exit")


# ================= AUTH =================

def register():

    username = input("Enter new username: ")
    password = getpass.getpass("Enter new password: ")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check existing username
    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        print("❌ Username already exists!")
        conn.close()
        return

    cursor.execute(
        "INSERT INTO users VALUES (?, ?)",
        (username, password)
    )

    conn.commit()
    conn.close()

    print("✅ Registered Successfully!")


def login():

    username = input("Username: ")
    password = getpass.getpass("Password: ")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        print("✅ Login Successful!")
        return True

    else:
        print("❌ Invalid Credentials")
        return False


# ================= ADD INCOME =================

def add_income():

    try:
        amount = float(input("Enter income amount: "))

    except ValueError:
        print("❌ Invalid Amount")
        return

    source = input("Enter income source: ")

    date, time = get_current_datetime()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO transactions(date,time,type,amount,detail)
    VALUES(?,?,?,?,?)
    """, (date, time, "income", amount, source))

    conn.commit()
    conn.close()

    print("✅ Income Added Successfully!")


# ================= ADD EXPENSE =================

def add_expense():

    try:
        amount = float(input("Enter expense amount: "))

    except ValueError:
        print("❌ Invalid Amount")
        return

    category = input(
        "Enter category (Food/Travel/Groceries): "
    )

    date, time = get_current_datetime()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO transactions(date,time,type,amount,detail)
    VALUES(?,?,?,?,?)
    """, (date, time, "expense", amount, category))

    conn.commit()
    conn.close()

    print("✅ Expense Added Successfully!")


# ================= VIEW TRANSACTIONS =================

def view_transactions():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions")

    rows = cursor.fetchall()

    if not rows:
        print("❌ No Transactions Available")
        conn.close()
        return

    print("\n================ TRANSACTIONS ================")

    print(
        f"{'ID':<5}{'DATE':<15}{'TIME':<12}{'TYPE':<12}{'AMOUNT':<12}{'DETAIL'}"
    )

    print("-" * 70)

    for row in rows:

        id_, date, time, type_, amount, detail = row

        print(
            f"{id_:<5}{date:<15}{time:<12}{type_:<12}₹{amount:<10.2f}{detail}"
        )

    conn.close()


# ================= VIEW BALANCE =================

def view_balance():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT SUM(amount) FROM transactions WHERE type='income'"
    )

    income = cursor.fetchone()[0]

    cursor.execute(
        "SELECT SUM(amount) FROM transactions WHERE type='expense'"
    )

    expense = cursor.fetchone()[0]

    income = income if income else 0
    expense = expense if expense else 0

    balance = income - expense

    print("\n========== BALANCE ==========")

    print(f"💰 Total Income  : ₹{income:.2f}")
    print(f"💸 Total Expense : ₹{expense:.2f}")
    print(f"📊 Balance       : ₹{balance:.2f}")

    conn.close()


# ================= SEARCH =================

def search_transactions():

    print("Search available: income / expense")

    search_type = input(
        "Enter type (income/expense): "
    ).lower()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM transactions
    WHERE LOWER(type)=?
    """, (search_type,))

    rows = cursor.fetchall()

    if rows:

        print(f"\n===== {search_type.upper()} TRANSACTIONS =====")

        for row in rows:
            print(row)

    else:
        print("❌ No Transactions Found")

    conn.close()


# ================= DELETE =================

def delete_transaction():

    view_transactions()

    try:
        id_delete = int(
            input("\nEnter Transaction ID to delete: ")
        )

    except ValueError:
        print("❌ Invalid ID")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM transactions WHERE id=?",
        (id_delete,)
    )

    conn.commit()
    conn.close()

    print("🗑️ Transaction Deleted Successfully!")


# ================= UPDATE TRANSACTION =================

def update_transaction():

    view_transactions()

    try:
        id_update = int(
            input("\nEnter Transaction ID to update: ")
        )

        new_amount = float(
            input("Enter new amount: ")
        )

    except ValueError:
        print("❌ Invalid Input")
        return

    new_detail = input(
        "Enter new detail/category: "
    )

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE transactions
    SET amount=?, detail=?
    WHERE id=?
    """, (new_amount, new_detail, id_update))

    conn.commit()
    conn.close()

    print("✅ Transaction Updated Successfully!")


# ================= MONTHLY REPORT =================

def monthly_report():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT detail,SUM(amount)
    FROM transactions
    WHERE type='expense'
    GROUP BY detail
    """)

    rows = cursor.fetchall()

    print("\n========== MONTHLY REPORT ==========")

    for detail, amount in rows:
        print(f"{detail:<15} : ₹{amount:.2f}")

    conn.close()


# ================= BUDGET CHECK =================

def budget_check():

    try:
        limit = float(
            input("Enter your monthly budget limit: ")
        )

    except ValueError:
        print("❌ Invalid Budget Amount")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(amount)
    FROM transactions
    WHERE type='expense'
    """)

    total_expense = cursor.fetchone()[0]

    total_expense = total_expense if total_expense else 0

    print(f"\n💸 Total Expense: ₹{total_expense:.2f}")

    if total_expense > limit:
        print("⚠️ Budget Limit Exceeded!")

    else:
        print("✅ Budget Under Control")

    conn.close()


# ================= EXPORT CSV =================

def export_to_csv():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions")

    rows = cursor.fetchall()

    with open(
        "transactions.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            ["ID", "DATE", "TIME", "TYPE", "AMOUNT", "DETAIL"]
        )

        writer.writerows(rows)

    conn.close()

    print("✅ Transactions Exported Successfully!")
    print("📁 File saved as transactions.csv")
    print("📂 Current Location:", os.getcwd())


# ================= PIE CHART =================

def expense_chart():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT detail,SUM(amount)
    FROM transactions
    WHERE type='expense'
    GROUP BY detail
    """)

    rows = cursor.fetchall()

    if not rows:
        print("❌ No Expense Data Available")
        conn.close()
        return

    categories = []
    amounts = []

    for detail, amount in rows:

        categories.append(detail)
        amounts.append(amount)

    plt.figure(figsize=(10, 10))

    plt.pie(
        amounts,
        labels=categories,
        autopct="%1.1f%%"
    )

    plt.title("Expense Distribution")

    plt.show()

    conn.close()


# ================= MAIN =================

init_db()

while True:

    print("\n========== MAIN MENU ==========")

    print("1.Register")
    print("2.Login")
    print("3.Exit")

    option = input("Choose an option: ")

    if option == "1":

        register()

    elif option == "2":

        if login():

            while True:

                menu()

                choice = input("Choose option: ")

                if choice == "1":
                    add_income()

                elif choice == "2":
                    add_expense()

                elif choice == "3":
                    view_transactions()

                elif choice == "4":
                    view_balance()

                elif choice == "5":
                    search_transactions()

                elif choice == "6":
                    delete_transaction()

                elif choice == "7":
                    update_transaction()

                elif choice == "8":
                    monthly_report()

                elif choice == "9":
                    budget_check()

                elif choice == "10":
                    expense_chart()

                elif choice == "11":
                    export_to_csv()

                elif choice == "12":

                    print("🔒 Logged Out Successfully!")
                    break

                elif choice == "13":

                    print("🙏 Thank You!")
                    exit()

                else:
                    print("❌ Invalid Choice")

    elif option == "3":

        print("🙏 Exiting Program...")
        break

    else:
        print("❌ Invalid Option")
