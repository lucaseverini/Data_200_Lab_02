# Summary: This module contains the user interface and logic for a graphical user interface version of the stock manager program.

from datetime import datetime
from os import path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, simpledialog, filedialog
import csv
import stock_data
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart, sortStocks, sortDailyData

class StockApp:
    def __init__(self):
        self.stock_list = []
        #check for database, create if not exists
        if path.exists("stocks.db") == False:
            stock_data.create_database()

 # This section creates the user interface

        # Create Window
        self.root = Tk()
        self.root.title("(myname) Stock Manager") #Replace with a suitable name for your program


        # Add Menubar
        self.menubar = Menu(self.root)

        # Add File Menu


        # Add Web Menu 


        # Add Chart Menu
 

        # Add menus to window       


        # Add heading information

        

        # Add stock list

        
        
        # Add Tabs
 
        

        # Set Up Main Tab


        # Setup History Tab

        
        
        # Setup Report Tab


        ## Call MainLoop
        self.root.mainloop()

# This section provides the functionality
       
    # Load stocks and history from database.
    def load(self):
        self.stockList.delete(0,END)
        stock_data.load_stock_data(self.stock_list)
        sortStocks(self.stock_list)
        for stock in self.stock_list:
            self.stockList.insert(END,stock.symbol)
        messagebox.showinfo("Load Data","Data Loaded")

    # Save stocks and history to database.
    def save(self):
        stock_data.save_stock_data(self.stock_list)
        messagebox.showinfo("Save Data","Data Saved")

    # Refresh history and report tabs
    def update_data(self, evt):
        self.display_stock_data()

    # Display stock price and volume history.
    def display_stock_data(self):
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
                self.dailyDataList.delete("1.0",END)
                self.stockReport.delete("1.0",END)
                self.dailyDataList.insert(END,"- Date -   - Price -   - Volume -\n")
                self.dailyDataList.insert(END,"=================================\n")
                for daily_data in stock.DataList:
                    row = daily_data.date.strftime("%m/%d/%y") + "   " +  '${:0,.2f}'.format(daily_data.close) + "   " + str(daily_data.volume) + "\n"
                    self.dailyDataList.insert(END,row)

                #display report


                    

    
    # Add new stock to track.
    def add_stock(self):
        new_stock = Stock(self.addSymbolEntry.get(),self.addNameEntry.get(),float(str(self.addSharesEntry.get())))
        self.stock_list.append(new_stock)
        self.stockList.insert(END,self.addSymbolEntry.get())
        self.addSymbolEntry.delete(0,END)
        self.addNameEntry.delete(0,END)
        self.addSharesEntry.delete(0,END)

    # Buy shares of stock.
    def buy_shares(self):
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.buy(float(self.updateSharesEntry.get()))
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
        messagebox.showinfo("Buy Shares","Shares Purchased")
        self.updateSharesEntry.delete(0,END)

    # Sell shares of stock.
    def sell_shares(self):
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.sell(float(self.updateSharesEntry.get()))
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
        messagebox.showinfo("Sell Shares","Shares Sold")
        self.updateSharesEntry.delete(0,END)

    # Remove stock and all history from being tracked.
    def delete_stock(self):
       pass

    # Get data from web scraping.
    def scrape_web_data(self):
        dateFrom = simpledialog.askstring("Starting Date","Enter Starting Date (m/d/yy)")
        dateTo = simpledialog.askstring("Ending Date","Enter Ending Date (m/d/yy")
        try:
            stock_data.retrieve_stock_web(dateFrom,dateTo,self.stock_list)
        except:
            messagebox.showerror("Cannot Get Data from Web","Check Path for Chrome Driver")
            return
        self.display_stock_data()
        messagebox.showinfo("Get Data From Web","Data Retrieved")

    # Import CSV stock history file.
    def importCSV_web_data(self):
        symbol = self.stockList.get(self.stockList.curselection())
        filename = filedialog.askopenfilename(title="Select " + symbol + " File to Import",filetypes=[('Yahoo Finance! CSV','*.csv')])
        if filename != "":
            stock_data.import_stock_web_csv(self.stock_list,symbol,filename)
            self.display_stock_data()
            messagebox.showinfo("Import Complete",symbol + "Import Complete")   
    
    # Display stock price chart.
    def display_chart(self):
        symbol = self.stockList.get(self.stockList.curselection())
        display_stock_chart(self.stock_list,symbol)


def main():
        app = StockApp()
        

if __name__ == "__main__":
    # execute only if run as a script
    main()