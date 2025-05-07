import stock_data
import stocks
from stock_class import Stock, DailyData

def main_menu():
    while True:
        print("\nStock Analyzer -")
        print("1 - Manage Stocks (Add, Update, Delete, List)")
        print("2 - Add Daily Stock Data (Date, Price, Volume)")
        print("3 - Show Report")
        print("4 - Show Chart")
        print("5 - Manage Data (Save, Load, Retrieve)")
        print("0 - Exit Program")
        choice = input("Enter Menu Option: ")
        
        if choice == '1':
            manage_stocks()
        elif choice == '2':
            add_daily_data()
        elif choice == '3':
            show_report()
        elif choice == '4':
            show_chart()
        elif choice == '5':
            manage_data()
        elif choice == '0':
            print("Exiting.")
            break
        else:
            print("Invalid input. Try again.")

def manage_stocks():
    while True:
        print("\nManage Stocks -")
        print("1 - Add Stock")
        print("2 - Update Shares")
        print("3 - Delete Stock")
        print("4 - List Stocks")
        print("0 - Exit Manage Stocks")
        choice = input("Enter Menu Option: ")
        
        if choice == '1':
            add_stock()
        elif choice == '2':
            update_shares()
        elif choice == '3':
            delete_stock()
        elif choice == '4':
            list_stocks()
        elif choice == '0':
            break
        else:
            print("Invalid input. Try again.")

def update_shares():
    while True:
        print("\nUpdate Shares -")
        print("1 - Buy Shares")
        print("2 - Sell Shares")
        print("0 - Exit Update Shares")
        choice = input("Enter Menu Option: ")

        if choice == '1':
            buy_shares()
        elif choice == '2':
            sell_shares()
        elif choice == '0':
            break
        else:
            print("Invalid input. Try again.")

def manage_data():
    while True:
        print("\nManage Data -")
        print("1 - Save Data to Database")
        print("2 - Load Data from Database")
        print("3 - Retrieve Data from Web")
        print("4 - Import from CSV File")
        print("0 - Exit Manage Data")
        choice = input("Enter Menu Option: ")

        if choice == '1':
            save_to_db()
        elif choice == '2':
            load_from_db()
        elif choice == '3':
            retrieve_from_web()
        elif choice == '4':
            import_csv()
        elif choice == '0':
            break
        else:
            print("Invalid input. Try again.")

# Placeholders for individual action functions
def add_stock():
    pass

def buy_shares():
    pass

def sell_shares():
    pass

def delete_stock():
    pass

def list_stocks():
    pass

def add_daily_data():
    pass

def show_report():
    pass

def show_chart():
    pass

def save_to_db():
    pass

def load_from_db():
    pass

def retrieve_from_web():
    pass

def import_csv():
    pass

if __name__ == "__main__":
    main_menu()
