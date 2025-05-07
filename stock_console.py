#!/usr/bin/env python3

# Lab2 (May-6-2025)
# Class: DATA 200-22
# Instructor: Paramdeep Saini paramdeep.saini@sjsu.edu
# Student: Luca Severini 008879273 luca.severini@sjsu.edu

# This module contains the user interface and logic for a console-based version of the stock manager program.

import sys
from datetime import datetime
from utilities import clear_screen, display_stock_chart, enter_stock
from os import path
from stock_data import load_stocks
from stock_data import save_stocks
from stock_data import add_stock_data
from stock_data import delete_stock_data
from stock_data import get_stock_list
from stock_data import get_stock_by_symbol
from stock_data import update_stock_amount
from stock_data import update_stock_price
from stock_data import add_stock_transaction
from stock_data import import_from_csv_file
from stock_data import export_to_csv_file
from web import get_stock_price
from web import get_stock_data
from stock_class import StockInfo
import utilities

# Main Menu
def main_menu():
    option = ""
    while option != "0":
        clear_screen()
        print("\nStock Analyzer ---")
        print("1 - Manage Stocks (Add, Update, Delete, List)")
        print("2 - Add Daily Stock Data (Date, Price, Volume)")
        print("3 - Stock Report")
        print("4 - Stock Chart")
        print("5 - Manage Data (Save, Load, Retrieve)")
        print("0 - Exit Program")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","5","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("Stock Analyzer ---")
            print("1 - Manage Stocks (Add, Update, Delete, List)")
            print("2 - Add Daily Stock Data (Date, Price, Volume)")
            print("3 - Show Report")
            print("4 - Show Chart")
            print("5 - Manage Data (Save, Load, Retrieve)")
            print("0 - Exit Program")
            option = input("Enter Menu Option: ")
        if option == "1":
            manage_stocks()
        elif option == "2":
            add_stock_daily_data()
        elif option == "3":
            display_report()
        elif option == "4":
            display_chart()
        elif option == "5":
            manage_data()
        else:
            clear_screen()
            print("Goodbye")

# Manage Stocks
def manage_stocks():
    option = ""
    while option != "0":
        clear_screen()
        print("\nManage Stocks ---")
        print("1 - Add Stock")
        print("2 - Update Shares")
        print("3 - Delete Stock")
        print("4 - List Stocks")
        print("0 - Exit Manage Stocks")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("1 - Add Stock")
            print("2 - Update Shares")
            print("3 - Delete Stock")
            print("4 - List Stocks")
            print("0 - Exit Manage Stocks")
            option = input("Enter Menu Option: ")
        if option == "1":
            add_stock()
        elif option == "2":
            update_shares()
        elif option == "3":
            delete_stock()
        elif option == "4":
            list_stocks()
        else:
            print("Returning to Main Menu")

# Add new stock to track
def add_stock():
    print("\nAdd Stock ---")
    while True:
        stock = enter_stock()
        if stock == None:
            break
        if add_stock_data(stock):
            print(f"Stock {stock.symbol} added") 
        else:
            print(f"Stock {stock.symbol} already present") 
        
# Buy or Sell Shares Menu
def update_shares():
    while True:
        print("\nUpdate Shares ---")
        print("1 - Buy Shares")
        print("2 - Sell Shares")
        print("3 - Update Price")
        print("0 - Exit Update Shares")
        choice = input("Enter Menu Option: ").strip()

        if choice == '1':
            buy_shares()
        elif choice == '2':
            sell_shares()
        elif choice == '3':
            update_price()
        elif choice == '0':
            break
        else:
            print("Invalid input.")

# Buy Shares (add to shares)
def buy_shares():
    print("\nBuy Shares ---")
    
    stock_list = get_stock_list()
    if not stock_list:
         print("No stock present.")
         return

    stock_list.sort(key = lambda s: s.symbol.upper())
    print("Stock list: [ " + ", ".join([stock.symbol for stock in stock_list]) + " ]")
    
    symbol = input("Which stock do you want to buy? [leave blank to exit] : ").strip().upper()
    if not symbol:
        return
        
    stock = get_stock_by_symbol(symbol)
    if not stock:
        print(f"Stock '{symbol}' not found.")
        return

    amount = float(input("How many shares do you want to buy? (0 to cancel) : ").strip())
    if amount <= 0:
        return

    date = datetime.today().strftime("%m/%d/%y")
    transaction = (stock.price, amount, date)
    if add_stock_transaction(symbol, transaction):
        print(f"Stock '{symbol}' transaction added")
    else:
        print(f"Stock '{symbol}' transactions not added.")
       
# Sell Shares (subtract from shares)
def sell_shares():
    print("\nSell Shares ---")
    
    stock_list = get_stock_list()
    if not stock_list:
         print("No stock present.")
         return

    stock_list.sort(key = lambda s: s.symbol.upper())
    print("Stock list: [ " + ", ".join([stock.symbol for stock in stock_list]) + " ]")

    symbol = input("Which stock do you want to sell? [leave blank to exit] : ").strip().upper()
    if not symbol:
        return
        
    stock = get_stock_by_symbol(symbol)
    if not stock:
        print(f"Stock '{symbol}' not found.")
        return

    print(f"Stock {symbol} amount: {stock.amount}")
    amount = float(input("How many shares do you want to sell? (0 to cancel) : ").strip())
    if amount <= 0:
        return
        
    if amount > stock.amount:
        print(f"Invalid amount.")
        return
        
    date = datetime.today().strftime("%m/%d/%y")
    transaction = (stock.price, -amount, date)
    if add_stock_transaction(symbol, transaction):
        print(f"Stock '{symbol}' transactions added")
    else:
        print(f"Stock '{symbol}' transactions not added.")

def update_price():
    print("\nUpdate Price ---")
    
    stock_list = get_stock_list()
    if not stock_list:
        print("No stock present.")
        return

    stock_list.sort(key = lambda s: s.symbol.upper())
    print("Stock list: [ " + ", ".join([stock.symbol for stock in stock_list]) + " ]")
    
    symbol = input("Which stock do you want to update price for? [leave blank to exit] : ").strip().upper()
    if not symbol:
        return
        
    stock = get_stock_by_symbol(symbol)
    if not stock:
        print(f"Stock '{symbol}' not found.")
        return

    new_price = 0
    while True:
        price_input = input("Enter new price (0 to fetch from web, blank to cancel) : ").strip()
        if not price_input:
            return

        new_price = float(price_input)
        if new_price < 0:
            print(f"Stock price cannot be negative")
        else:
            break
        
    if new_price == 0:
        print(f"Getting {symbol} price from Yahoo! Finance...")
        new_price = get_stock_price(symbol)
        if new_price is None:
            print(f"Could not fetch price for '{symbol}'.")
            return
        print(f"Fetched price for '{symbol}': {new_price}")

    if update_stock_price(symbol, new_price):
        print(f"Stock '{symbol}' price updated to: {new_price}")
    else:
        print(f"Stock '{symbol}' price not updated.")
     
# Remove stock and all daily data
def delete_stock():
    print("\nDelete Stock ---")
    stock_list = get_stock_list()
    if not stock_list:
         print("No stock present.")
         return

    stock_list.sort(key = lambda s: s.symbol.upper())
    print("Stock list: [ " + ", ".join([stock.symbol for stock in stock_list]) + " ]")

    symbol = input("Enter stock symbol to delete [leave blank to exit] : ").strip().upper()
    if not symbol:
        print("Delete canceled.")
    else:
        if delete_stock_data(symbol):
            print(f"Stock {symbol} deleted")
        else:
            print(f"Stock {symbol} not found.")
            
# List stocks being tracked
def list_stocks():
    clear_screen()
    print("\nList Stocks ---")
    print(f"{'SYMBOL':<10}{'NAME':<20}{'PRICE':>10}{'SHARES':>12}{'VALUE':>12}")
    print("=" * 64)
    stock_list = get_stock_list()
    if stock_list:
        stock_list.sort(key = lambda s: s.symbol.upper())
        for stock in stock_list:
            value = stock.price * stock.amount if stock.price and stock.amount else 0
            print(f"{stock.symbol:<10}{stock.company:<20}{stock.price:>10.2f}{stock.amount:>12.1f}{value:>12.2f}")
 
            if stock.transactions:
                stock.transactions.sort(key = lambda t: datetime.strptime(t[2], "%m/%d/%y"))
                
                print(f"{'':>36}DATE{'' :>7}PRICE{'' :>6}VOLUME")
                print(f"{'':>33}{'-' * 31}")
                for price, volume, date in stock.transactions:
                    print(f"{'':>33}{date:>8}{price:>11.2f}{volume:>12.1f}")
            else:
                print(f"{'':>33}No transactions.")          
            print()
    else:
        print("No stock present.")

# Add Daily Stock Data
def add_stock_daily_data():
    clear_screen()
    print("\nAdd Daily Stock Data ---")   
    stock_list = get_stock_list()
    if not stock_list:
        print("No stock present.")
        return

    stock_list.sort(key = lambda s: s.symbol.upper())
    print("Stock list: [ " + ", ".join([stock.symbol for stock in stock_list]) + " ]")
    
    symbol = input("Which stock do you want to use? [leave blank to exit] : ").strip().upper()
    if not symbol:
        return

    stock = get_stock_by_symbol(symbol)
    if not stock:
        print(f"Stock '{symbol}' not found.")
        return

    print(f"Ready to add data for: {symbol}")
    print("Enter Data Separated by Commas")
    print("Example: 8/28/20,47.85,10550")

    while True:
        line = input("Enter Date,Price,Volume [leave blank to exit]: ").strip()
        if not line:
            break
        try:
            date_input, price_input, volume_input = line.split(",")
            
            datetime.strptime(date_input.strip(), "%m/%d/%y")  # validate
            price = float(price_input.strip())
            volume = float(volume_input.strip())
 
            transaction = (price, volume, date_input)
            if add_stock_transaction(symbol, transaction):
                print(f"Stock '{symbol}' transactions added")
            else:
                print(f"Stock '{symbol}' transactions not added.")

        except ValueError:
            print("Invalid format. Use: MM/DD/YY,price,volume")

# Display Report for stock
def display_report():
    clear_screen()
    print("\nStock Report ---")
    stock_list = get_stock_list()
    if not stock_list:
        print("No stock present.")
        return

    stock_list.sort(key = lambda s: s.symbol.upper())
    
    while True:
        print("Stock list: [ " + ", ".join([stock.symbol for stock in stock_list]) + " ]")

        symbol = input("For which stock do you want the report? [leave blank to exit] : ").strip().upper()
        if not symbol:
            return
        
        stock = get_stock_by_symbol(symbol)
        if stock:
            print(f"\nReport for: {stock.symbol} {stock.company}")
            print(f"Shares: {stock.amount}")
            print(f"Price:  ${stock.price}")
            print(f"Transactions: {len(stock.transactions)}")

            print(f"{'DATE':>12}{'PRICE':>12}{'VOLUME':>12}")
            print("-" * 36)

            if stock.transactions:
                for price, volume, date in stock.transactions:
                    print(f"{date:>12}{price:>12.2f}{volume:>12.1f}")
            else:
                print("No transactions.")
            print("\n- Report Complete -\n")
        
        else:
            print(f"Stock '{symbol}' not found.")
 
# Show Chart for Ststockock
def display_chart():
    clear_screen()
    print("\nStock Chart ---")
    stock_list = get_stock_list()
    if not stock_list:
        print("No stock present.")
        return

    stock_list.sort(key = lambda s: s.symbol.upper())
 
    while True:
        print("Stock list: [ " + ", ".join([stock.symbol for stock in stock_list]) + " ]")
    
        symbol = input("For which stock do you want the report? [leave blank to exit] : ").strip().upper()
        if not symbol:
            return

        stock = get_stock_by_symbol(symbol)
        if stock:
            display_stock_chart(stock)
        else:
            print(f"Stock '{symbol}' not found.")

# Manage Data Menu
def manage_data():
    option = ""
    while option != "0":
        clear_screen()
        print("\nManage Data ---")
        print("1 - Save to Database")
        print("2 - Load from Database")
        print("3 - Retrieve from Web")
        print("4 - Import from CSV File")
        print("5 - Export to CSV File")
        print("0 - Exit Manage Data")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","5","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("1 - Save Data to Database")
            print("2 - Load Data from Database")
            print("3 - Retrieve Data from Web")
            print("4 - Import from CSV File")
            print("5 - Export to CSV File")
            print("0 - Exit Manage Data")
            option = input("Enter Menu Option: ")
        if option == "1":
            save_data_to_db()
        elif option == "2":
            load_data_from_db()
        elif option == "3":
            load_data_from_web()
        elif option == "4":
            import_csv()
        elif option == "5":
            export_csv()
        else:
            print("Returning to Main Menu")

# Load data from db
def load_data_from_db():
    print("\nLoad from Database ---")
    if load_stocks():
        save_stocks()
        print(f"Data loaded from Database")     

# Save data to db
def save_data_to_db():
    print("\nSave to Database ---")
    if save_stocks():
        print(f"Data saved to Database")     
    pass

# Load data from Yahoo! Finance using Web Scraping
def load_data_from_web():
    print("\nRetrieve Data from Web ---")
    line = input("Enter stock symbols separated by commas [leave blank to cancel] : ").strip()
    if not line:
        return []
    symbols = [s.strip().upper() for s in line.split(",") if s.strip()]    
    if not symbols:
        print("No stocks entered.")
        return

    symbols.sort()
    print("Stock list: [ " + ", ".join([symbol for symbol in symbols]) + " ]")

    symbols_data = []
    print(f"Fetching stock data (it can take a while or even fail - [Control-C to stop fetching data])")
    for symbol in symbols:
        try:
            print(f"Fetching {symbol} stock data...")
            data = get_stock_data(symbol)
            if data:
                symbols_data.append(data)
            else:
                print(f"{symbol} stock data not fetched")
        except KeyboardInterrupt:
            print(f"\nFetching {symbol} stock data interrupted.")
 
    for data in symbols_data:       
        symbol = data['symbol']       
        company =  data['company']
        price = data['price']       
        if None in (symbol, company, price):
            continue

        stock = StockInfo(symbol, company, float(price), float(0))
        if add_stock_data(stock):
            print(f"Stock {symbol} added") 
        else:
            print(f"Stock {symbol} already present") 

# Import stock price and volume history using CSV Import
def import_csv():
    print("\nImport from CSV file ---")
    filename = input("Enter CSV file name to import [blank to cancel]: ").strip()
    if not filename:
        print("Import canceled.")
        return
        
    if import_from_csv_file(filename):
        save_stocks()
        print(f"Data imported from CSV {filename}")  

# Export stock price and volume history using CSV Import
def export_csv():
    print("\nExport to CSV file ---")
    filename = input("Enter CSV file name to export [blank to cancel]: ").strip()
    if not filename:
        print("Export canceled.")
        return
        
    if export_to_csv_file(filename):
        print(f"Data exported to CSV {filename}")  

# Begin program
def main():
    try:
        load_stocks()
        main_menu() 
        save_stocks()

    except KeyboardInterrupt:
        print("\nProgram interrupted.")
        sys.exit(1)

    except Exception as e:
        print(f"\nUnexpected error occurred: {e}")
        sys.exit(1)

# Program Starts Here
if __name__ == "__main__":
    try:
        main()
        sys.exit(0)

    except KeyboardInterrupt:
        print("\nProgram interrupted.")
        sys.exit(1)

    except Exception as e:
        print(f"\nUnexpected error occurred: {e}")
        sys.exit(1)
