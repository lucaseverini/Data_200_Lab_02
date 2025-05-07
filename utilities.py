#!/usr/bin/env python3

# Lab2 (May-6-2025)
# Class: DATA 200-22
# Instructor: Paramdeep Saini paramdeep.saini@sjsu.edu
# Student: Luca Severini 008879273 luca.severini@sjsu.edu

# Helper Functions

import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from stock_class import StockInfo
from web import get_stock_price
from os import system, name

# Function to Clear the Screen
# ==============================================================================
def clear_screen():
    return
    if name == "nt": # User is running Windows
        _ = system('cls')
    else: # User is running Linux or Mac
        _ = system('clear')

# Function to sort the stock list (alphabetical)
# ==============================================================================
def sortStocks(stock_list):
    stock_list.sort(key=lambda s: s.symbol.upper())
    pass

# Function to sort the daily stock data (oldest to newest) for all stocks
# ==============================================================================
def sortDailyData(stock_list):
    for stock in stock_list:
        stock.transactions.sort(key=lambda t: datetime.strptime(t[2], "%m/%d/%y"))
        
# Enter a new stock        
# ==============================================================================
def enter_stock():
    symbol = input("Enter stock symbol [leave blank to exit] : ").strip().upper()
    if not symbol:
        return None
        
    company = ""
    while True:
        company = input(f"Enter company name for {symbol}: ").strip()
        if company:
            break
        print(f"Company name cannot be empty")
    
    while True:
        price_input = input("Enter price [enter 0 to get it from Yahoo! Finance]: ").strip()
        price = float(price_input) if price_input else 0
        if price == 0:
            print(f"Getting {symbol} price from Yahoo! Finance...")
            price = get_stock_price(symbol)
            if price is None:
                print("Failed to fetch price. You can enter it manually.")
                price = float(input("Enter price manually: ").strip())
            else:
                print(f"Retrieved price for {symbol}: {price}")
        if price != 0:
            break
        
    amount_input = input("Enter number of shares (0 if none): ").strip()
    amount = float(amount_input) if amount_input else 0.0
    
    stock = StockInfo(symbol, company, price, amount)
    
    if amount > 0:
        date = input("Enter date (MM/DD/YY) [leave blank for today]: ").strip()
        if not date:
            date = datetime.today().strftime("%m/%d/%y")
        else:
            try:
                datetime.strptime(date, "%m/%d/%y")  # validate               
                
            except ValueError:
                print("Invalid date format. Using today's date.")
                date = datetime.today().strftime("%m/%d/%y")
                
        stock.add_transaction(price, amount, date)
 
    print("Stock created:")
    print(stock)
    return stock

# Function to create stock chart
# ==============================================================================
def display_stock_chart(stock):
    if not stock.transactions:
        print(f"Stock '{symbol}' has no transactions to plot.")
        return
        
    print(f"Plotting chart for stock '{stock.symbol}'...")

    df = pd.DataFrame(stock.transactions, columns=["Price", "Volume", "Date"])
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%y")
    df = df.sort_values("Date")

    plt.figure(figsize=(8, 5))
    plt.plot(df["Date"], df["Price"], marker="", linestyle="-")
    plt.title(stock.company.upper())
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    plt.tight_layout()
    
    plt.tight_layout()
    plt.show(block=False)
    plt.pause(0.1)
