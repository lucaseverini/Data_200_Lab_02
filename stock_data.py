#!/usr/bin/env python3

# Lab2 (May-6-2025)
# Class: DATA 200-22
# Instructor: Paramdeep Saini paramdeep.saini@sjsu.edu
# Student: Luca Severini 008879273 luca.severini@sjsu.edu

# This module contains the functions used by both console and GUI programs to manage stock data.

import sqlite3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import csv
import time
from datetime import datetime
from utilities import clear_screen
from utilities import sortDailyData
from stock_class import StockInfo
import pickle
from pathlib import Path
import csv

STOCK_FILE = "STOCK_DATA.dat"
STOCK_DB = []

# Import data from CSV file
# ==============================================================================
def export_to_csv_file(filename):
    try:
        with open(filename, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Symbol", "Company", "Price", "Volume", "Date"])

            for stock in STOCK_DB:
                for price, volume, date in stock.transactions:
                    writer.writerow([stock.symbol, stock.company, price, volume, date])
        return True
        
    except Exception as e:
        print(f"Export to {filename} failed: {e}")
        return False
        
# Import data from CSV file
# ==============================================================================
def import_from_csv_file(filename):
    try:
        with open(filename, newline = '') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header

            for row in reader:
                if len(row) < 5:
                    continue
                symbol, company, price, volume, date = row[0:5]
                stock = get_stock_by_symbol(symbol)
                if not stock:
                    stock = StockInfo(symbol, company)
                    STOCK_DB.append(stock)
                stock.add_transaction(price = price, volume = volume, date = date)
        return True
        
    except Exception as e:
        print(f"Import from {filename} failed: {e}")
        return False
        
# Load the stock DB
# ==============================================================================
def load_stocks():
    if Path(STOCK_FILE).exists():
        global STOCK_DB
        STOCK_DB = load_from_file()
        return True
    else:
        return False
        
# Save the stock DB
# ==============================================================================
def save_stocks():
    return save_to_file(STOCK_DB)
 
# Save a list of StockInfo objects to a binary file
# ==============================================================================
def save_to_file(stock_list, filename = STOCK_FILE):
    try:
        with open(filename, 'wb') as f:
            pickle.dump(stock_list, f)
        return True
        
    except Exception as e:
        print(f"Failed to save stock data: {e}")
        return False

# Load a list of StockInfo objects from a binary file
# ==============================================================================
def load_from_file(filename = STOCK_FILE):
    if not Path(filename).exists():
        print(f"No data file found at {filename}. Returning empty list.")
        return []

    try:
        with open(filename, 'rb') as f:
            stock_list = pickle.load(f)
        # print(f"Loaded {len(stock_list)} stock(s) from {filename}")
        return stock_list
        
    except Exception as e:
        print(f"Failed to load stock data: {e}")
        return []  
        
# Create the SQLite database
# ==============================================================================
def create_database():
    stockDB = "stocks.db"
    conn = sqlite3.connect(stockDB)
    cur = conn.cursor()
    createStockTableCmd = """CREATE TABLE IF NOT EXISTS stocks (
                            symbol TEXT NOT NULL PRIMARY KEY,
                            name TEXT,
                            shares REAL
                        );"""
    createDailyDataTableCmd = """CREATE TABLE IF NOT EXISTS dailyData (
                                symbol TEXT NOT NULL,
                                date TEXT NOT NULL,
                                price REAL NOT NULL,
                                volume REAL NOT NULL,
                                PRIMARY KEY (symbol, date)
                        );"""   
    cur.execute(createStockTableCmd)
    cur.execute(createDailyDataTableCmd)

# Save stocks and daily data into database
# ==============================================================================
def save_stock_data(stock_list):
    stockDB = "stocks.db"
    conn = sqlite3.connect(stockDB)
    cur = conn.cursor()
    insertStockCmd = """INSERT INTO stocks
                            (symbol, name, shares)
                            VALUES
                            (?, ?, ?); """
    insertDailyDataCmd = """INSERT INTO dailyData
                                    (symbol, date, price, volume)
                                    VALUES
                                    (?, ?, ?, ?);"""
    for stock in stock_list:
        insertValues = (stock.symbol, stock.name, stock.shares)
        try:
            cur.execute(insertStockCmd, insertValues)
            cur.execute("COMMIT;")
        except:
            pass
        for daily_data in stock.DataList: 
            insertValues = (stock.symbol,daily_data.date.strftime("%m/%d/%y"),daily_data.close,daily_data.volume)
            try:
                cur.execute(insertDailyDataCmd, insertValues)
                cur.execute("COMMIT;")
            except:
                pass
    
# Load stocks and daily data from database
def load_stock_data(stock_list):
    stock_list.clear()
    stockDB = "stocks.db"
    conn = sqlite3.connect(stockDB)
    stockCur = conn.cursor()
    stockSelectCmd = """SELECT symbol, name, shares
                    FROM stocks; """
    stockCur.execute(stockSelectCmd)
    stockRows = stockCur.fetchall()
    for row in stockRows:
        new_stock = Stock(row[0],row[1],row[2])
        dailyDataCur = conn.cursor()
        dailyDataCmd = """SELECT date, price, volume
                        FROM dailyData
                        WHERE symbol=?; """
        selectValue = (new_stock.symbol)
        dailyDataCur.execute(dailyDataCmd,(selectValue,))
        dailyDataRows = dailyDataCur.fetchall()
        for dailyRow in dailyDataRows:
            daily_data = DailyData(datetime.strptime(dailyRow[0],"%m/%d/%y"),float(dailyRow[1]),float(dailyRow[2]))
            new_stock.add_data(daily_data)
        stock_list.append(new_stock)
    sortDailyData(stock_list)

# Get stock price history from web using Web Scraping
# ==============================================================================
def retrieve_stock_web(dateStart,dateEnd,stock_list):
    dateFrom = str(int(time.mktime(time.strptime(dateStart,"%m/%d/%y"))))
    dateTo = str(int(time.mktime(time.strptime(dateEnd,"%m/%d/%y"))))
    recordCount = 0
    for stock in stock_list:
        stockSymbol = stock.symbol
        url = "https://finance.yahoo.com/quote/"+stockSymbol+"/history?period1="+dateFrom+"&period2="+dateTo+"&interval=1d&filter=history&frequency=1d"
        # Note this code assumes the use of the Chrome browser.
        # You will have to modify if you are using a different browser.
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches',['enable-logging'])
        options.add_experimental_option("prefs",{'profile.managed_default_content_settings.javascript': 2})
        try:
            driver = webdriver.Chrome(options=options)
            driver.implicitly_wait(60)
            driver.get(url)
        except:
            raise RuntimeWarning("Chrome Driver Not Found")

        soup = BeautifulSoup(driver.page_source,"html.parser")
        row = soup.find('table',class_="W(100%) M(0)")
        dataRows = soup.find_all('tr')
        for row in dataRows:
            td = row.find_all('td')
            rowList = [i.text for i in td]
            columnCount = len(rowList)
            if columnCount == 7: # This row is a standard data row (otherwise it's a special case such as dividend which will be ignored)
                daily_data = DailyData(datetime.strptime(rowList[0],"%b %d, %Y"),float(rowList[5].replace(',','')),float(rowList[6].replace(',','')))
                stock.add_data(daily_data)
                recordCount += 1
    return recordCount

# Get price and volume history from Yahoo! Finance using CSV import
# ==============================================================================
def import_stock_web_csv(stock_list, symbol, filename):
    for stock in stock_list:
            if stock.symbol == symbol:
                with open(filename, newline='') as stockdata:
                    datareader = csv.reader(stockdata,delimiter=',')
                    next(datareader)
                    for row in datareader:
                        daily_data = DailyData(datetime.strptime(row[0],"%Y-%m-%d"),float(row[4]),float(row[6]))
                        stock.add_data(daily_data)

# ==============================================================================
def get_stock_by_symbol(symbol):  
    symbol = symbol.upper()
    stock_list = STOCK_DB
    for stock in stock_list:
        if stock.symbol == symbol:
            return stock
    return None

# ==============================================================================
def update_stock_amount(symbol, amount):  
    stock = next((s for s in STOCK_DB if s.symbol == symbol), None)
    if stock:
        stock.amount = amount
        save_stocks()
        return True
    else:
        return False

# ==============================================================================
def update_stock_price(symbol, price):  
    stock = next((s for s in STOCK_DB if s.symbol == symbol), None)
    if stock:
        stock.price = price
        save_stocks()
        return True
    else:
        return False

# ==============================================================================
def add_stock_transaction(symbol, transaction):  
    stock = next((s for s in STOCK_DB if s.symbol == symbol), None)
    if stock:
        stock.transactions.append(transaction)
        stock.amount = sum(volume for _, volume, _ in stock.transactions)
        save_stocks()
        return True
    else:
        return False

# ==============================================================================
def add_stock_data(stock):  
    if not get_stock_by_symbol(stock.symbol):
        STOCK_DB.append(stock)
        save_stocks()
        return True
    else:
        return False

# ==============================================================================
def delete_stock_data(symbol):  
    stock = get_stock_by_symbol(symbol)
    if stock:
        STOCK_DB.remove(stock)
        save_stocks()
        return True
    else:
        return False

# ==============================================================================
def get_stock_list():
    return STOCK_DB
    
# Main
# ==============================================================================
def main():
    clear_screen()
    print("This module will handle data storage and retrieval.")

if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()