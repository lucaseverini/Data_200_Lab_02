#!/usr/bin/env python3

# Lab2 (May-6-2025)
# Class: DATA 200-22
# Instructor: Paramdeep Saini paramdeep.saini@sjsu.edu
# Student: Luca Severini 008879273 luca.severini@sjsu.edu

# This module contains the class definitions that will be used in the stock analysis program

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
