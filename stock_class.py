#!/usr/bin/env python3

# Lab2 (May-6-2025)
# Class: DATA 200-22
# Instructor: Paramdeep Saini paramdeep.saini@sjsu.edu
# Student: Luca Severini 008879273 luca.severini@sjsu.edu

# Class for the Stock data
class StockInfo:
    def __init__(self, symbol, company, price = 0.0, amount = 0.0):
        self.symbol = symbol.upper()
        self.company = company
        self.price = float(price)
        self.amount = float(amount)
        self.transactions = []  # list of (price, volume, date)
    
    def add_transaction(self, price, volume, date):
        volume = float(volume)
        price = float(price)
        self.transactions.append((price, volume, date))
        self.amount = sum(volume for _, volume, _ in self.transactions)

    def __str__(self):
        return f"{self.symbol} ({self.company}) — Price: {self.price}, Amount: {self.amount}"

    def to_dict(self):
        return {
            "symbol": self.symbol,
            "company": self.company,
            "price": self.price,
            "amount": self.amount,
            "transactions": self.transactions
        }

    @staticmethod
    def from_dict(d):
        stock = StockInfo(
            symbol=d.get("symbol"),
            company=d.get("company"),
            price=d.get("price"),
            amount=d.get("amount")
        )
        stock.transactions = d.get("transactions", [])
        return stock

# Unit Test - Do Not Change Code Below This Line *** *** *** *** *** *** *** *** ***
# main() is used for unit testing only. It will run when stock_class.py is run.
# Run this to test your class code. Once you have eliminated all errors, you are
# ready to continue with the next part of the project.

def main():
    error_count = 0
    error_list = []
    print("Unit Testing Starting---")
    # Test Add Stock
    print("Testing Add Stock...",end="")
    try:
        testStock = Stock("TEST","Test Company",100)
        print("Successful!")
    except:
        print("***Adding Stock Failed!")
        error_count = error_count+1
        error_list.append("Stock Constructor Error")
    # Test Change Symbol
    print("Testing Change Symbol...",end="") 
    try:
        testStock.symbol = "NEWTEST"
        print("***ERROR! Changing stock symbol should not be allowed.")
        error_count = error_count+1
        error_list.append("Stock symbol change allowed. Stock symbol changes should not be allowed.")
    except:
        print("Successful! - Stock symbol change blocked")
    # Test Change Name
    print("Test Change Name...",end="")
    try:
        testStock.name = "New Test Company"
        if testStock.name == "New Test Company":
            print("Successful!")
        else:
            print("***ERROR! Name change unsuccessful.")
            error_count = error_count+1
            error_list.append("Name Change Error")
    except:
        print("***ERROR! Name change failed.")
        error_count = error_count+1
        error_list.append("Name Change Failure")
    # Test Change Shares
    print("Test Change Shares...",end="")
    try:
        testStock.shares = 200
        print("***ERROR! Changing stock shares directly should not be allowed.")
        error_count = error_count+1
        error_list.append("Stock shares change allowed. Change in shares should be done through buy() or sell().")
    except:
        print("Successful! - Stock shares change blocked")
    # Test Buy and Sell
    print("Test Buy shares...",end="")
    try:
        testStock.buy(50)
        if testStock.shares == 150:
            print("Successful!")
        else:
            print("***ERROR! Buy shares unsuccessful.")
            error_count = error_count + 1
            error_list.append("Buy Shares Failure!")
    except:
        print("***ERROR! Buy shares failed.")
        error_count = error_count + 1
        error_list.append("Buy Shares Failure!")
    print("Test Sell shares...",end="")
    try:
        testStock.sell(25)
        if testStock.shares == 125:
            print("Successful!")
        else:
            print("***ERROR! Sell shares unsuccessful.")
            error_count = error_count+1
            error_list.append("Sell Shares Failure!")
    except:
        print("***ERROR! Sell shares failed.")
        error_count = error_count + 1
        error_list.append("Sell Shares Failure!")

    # Test add daily data
    print("Creating daily stock data...",end="")
    daily_data_error = False
    try:
        dayData = DailyData(datetime.strptime("1/1/20","%m/%d/%y"),float(14.50),float(100000))
        testStock.add_data(dayData)
        if testStock.DataList[0].date != datetime.strptime("1/1/20","%m/%d/%y"):
            error_count = error_count + 1
            daily_data_error = True
            error_list.append("Add Daily Data - Problem with Date")
        if testStock.DataList[0].close != 14.50:
            error_count = error_count + 1
            daily_data_error = True
            error_list.append("Add Daily Data - Problem with Closing Price")
        if testStock.DataList[0].volume != 100000:
            error_count = error_count + 1
            daily_data_error = True
            error_list.append("Add Daily Data - Problem with Volume")  
    except:
        print("***ERROR! Add daily data failed.")
        error_count = error_count + 1
        error_list.append("Add daily data Failure!")
        daily_data_error = True
    if daily_data_error == True:
        print("***ERROR! Creating daily data failed.")
    else:
        print("Successful!")
    
    if (error_count) == 0:
        print("Congratulations - All Tests Passed")
    else:
        print("-=== Problem List - Please Fix ===-")
        for em in error_list:
            print(em)
    print("Goodbye")

# Program Starts Here
if __name__ == "__main__":
    # run unit testing only if run as a stand-alone script
    main()