import os
import csv
from datetime import datetime
def init_file():
    file_exists=os.path.isfile("transactions.csv")
    if not file_exists or os.path.getsize("transactions.csv")==0:
        with open("transactions.csv","w",newline="")as file:
            writer=csv.writer(file)
            writer.writerow(["date","time","type","amount","detail"])
def menu():
    print("\n==Welcome to Expense Tracker==")
    print("1.Add Income")
    print("2.Add Expense")
    print("3.View Transactions")
    print("4.View Balance")
    print("5.View search transactions by Type(income/expense):")
    print("6.Logout")
    print("7.Exit")
def register():
    username=input("Enter new username:")
    password=input("Enter new password:")
    with open("users.txt","a")as file:
        file.write(f"{username},{password}\n")
    print("Registered successfully!")

def login():
    username=input("username:")
    password=input("password:")
    try:
        with open("users.txt","r")as file:
            for line in file:
                if "," not in line:
                    continue
                u,p=line.strip().split(",")
                if u==username and p==password:
                    print("login successfull!\n")
                    return True
    except FileNotFoundError:
        print("No users found please register first")
    print("Invalid credentials")
    return False
      
def add_income():
    amount=float(input("Enter income amount:"))
    source=input("Enter income source:")
    now=datetime.now()
    date=now.strftime("%y-%m-%d")
    time=now.strftime("%H:%M:%S")
    with open("transactions.csv","a",newline="")as file:
        writer=csv.writer(file)
        writer.writerow([date,time,"income",amount,source])
    print("Income added successfully!")

def add_expense():
    amount=float(input("Enter expense amount:"))
    category=input("Enter expense category (Food,Travel,Groceries):")
    now=datetime.now()
    date=now.strftime("%y-%m-%d")
    time=now.strftime("%H:%M:%S")
    with open("transactions.csv","a",newline="")as file:
        writer=csv.writer(file)
        writer.writerow([date,time,"expense",amount,category])
    print("Expense added successfully!")

def view_transactions():
    print("\n--All Transactions--")
    try:
        with open("transactions.csv","r")as file:
            reader=csv.reader(file)
            print(f"{'date':<12}{'time':<8}{'type':<8}{'amount':<10}{'detail'}")
            print("-"*60)
            for row in reader:
                if len(row)==5:
                    date,time,trans_type,amount,detail=row
                    print(f"{date:<12}|{time:<8}|{trans_type:<8}|₹{amount:<10}|{detail}")
                else:
                    print("skipped a row")
    except FileNotFoundError:
        print("No transactions found!")

def view_balance():
    income = 0
    expense = 0
    try:
        with open("transactions.csv", "r") as file:
            reader=csv.reader(file)
            next(reader)
            for row in reader:
                type_=row[2]
                amount=float(row[3])
                if type_ == "income":
                    income +=(amount)
                elif type_ == "expense":
                    expense += (amount)
        balance=income-expense
        print(f"\n💰 Total Income  : ₹{income}")
        print(f"💸 Total Expense : ₹{expense}")
        print(f"📊 Balance       : ₹{income - expense}")
    except FileNotFoundError:
        print("⚠️ No data found.")

def search_transactions():
    search_type=input("Enter the type to search (Income/Expense):").lower()
    found=False
    print(f"\n---{search_type}transactions---")
    try:
        with open("transactions.csv","r")as file:
                  for line in file:
                      parts=line.strip().split(',')
                      if len(parts)==5 and parts[2].strip().lower()==search_type.strip().lower():
                          print(f"{parts[0]}{parts[1]}|{parts[2]:<8}{parts[3]}-{parts[4]}")
                          found=True
                  if not found:
                      print(f"No{search_type}transactions found")
    except FileNotFoundError:
        print("No transactions found")
                             
init_file()
while True:
    print("\n==Welcome to Expense Tracker==")
    print("1.Register")
    print("2.Login")
    print("3.Exit")

    option=input("choose an option(1-3):")
    if option=="1":
        register()
    elif option=="2":
        if login():
            while True:
                menu()
                choice = input("Choose an option (1–6): ")
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
                    print("Logged out.Returning to main menu.\n")
                elif choice == "7":
                    print("Exiting Thankyou!")
                    break
                else:
                    print("❌ Invalid choice. Try again.")
    elif option=="3":
        print("Thankyou!Exiting...")
        break
    else:
        print("Invalid choice.Try again")
    




        
