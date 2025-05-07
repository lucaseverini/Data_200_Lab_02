#!/usr/bin/env python3

# Lab2 (May-6-2025)
# Class: DATA 200-22
# Instructor: Paramdeep Saini paramdeep.saini@sjsu.edu
# Student: Luca Severini 008879273 luca.severini@sjsu.edu

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
            
def get_stock_price(symbol):
    try:
        options = Options()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        
        url = f"https://finance.yahoo.com/quote/{symbol}"
        driver.get(url)

        driver.implicitly_wait(3)
        
        selector = f"fin-streamer[data-field='regularMarketPrice'][data-symbol='{symbol}']"       
        price_element = driver.find_element(By.CSS_SELECTOR, selector)
        price_element_text = price_element.text.replace(',', '') # Remove commas
        price = float(price_element_text)
        return price
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
        
    finally:
        if 'driver' in locals() and driver:
            driver.quit()
            
def get_stock_info(symbol):
    try:
        options = Options()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)

        url = f"https://finance.yahoo.com/quote/{symbol}"
        driver.get(url)

        driver.implicitly_wait(3)

        # Get the stock price
        price_selector = f"fin-streamer[data-field='regularMarketPrice'][data-symbol='{symbol}']"
        price_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, price_selector))
        )
        price = float(price_element.text)

        # Get the company name - trying a broader selector
        name_selector = "h1.yf-xxbei9"
        try:
            name_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, name_selector))
            )
            company_name_parts = name_element.text.split(" (")
            company_name = company_name_parts[0].strip() if company_name_parts else None
        except:
            company_name = None
            print(f"Could not find company name using selector: {name_selector}")

        return {"symbol": symbol, "price": price, "company": company_name}

    except Exception as e:
        print(f"An error occurred while fetching data for {symbol}: {e}")
        return {"symbol": symbol, "price": None, "company_name": None}

    finally:
        if 'driver' in locals() and driver:
            driver.quit()

def get_stock_data(symbol):
    stock_data = {"symbol": symbol, "company": None, "price": None,
                  "regular_market_change": None, "regular_market_change_percent": None,
                  "post_market_price": None, "post_market_change": None,
                  "post_market_change_percent": None}
    try:
        options = Options()
        options.add_argument("--headless=new")
        service = Service()
        driver = webdriver.Chrome(service=service, options=options)

        url = f"https://finance.yahoo.com/quote/{symbol}"
        driver.get(url)

        driver.implicitly_wait(5)

        # Get the company name
        name_selector = "h1.yf-xxbei9"
        try:
            name_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, name_selector))
            )
            company_name_parts = name_element.text.split(" (")
            stock_data["company"] = company_name_parts[0].strip() if company_name_parts else None
        except:
            print(f"Could not find company name using selector: {name_selector}")

        # Get regular market price
        price_selector = "[data-testid='qsp-price']"
        try:
            price_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, price_selector))
            )
            price_element_text = price_element.text.replace(',', '') # Remove commas
            stock_data["price"] = float(price_element.text)

        except:
            print(f"Could not find regular market price using selector: {price_selector}")

        # Get regular market change
        change_selector = "[data-testid='qsp-price-change']"
        try:
            change_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, change_selector))
            )
            stock_data["regular_market_change"] = float(change_element.text)
        except:
            print(f"Could not find regular market change using selector: {change_selector}")

        # Get regular market change percent
        change_percent_selector = "[data-testid='qsp-price-change-percent']"
        try:
            change_percent_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, change_percent_selector))
            )
            # Remove parentheses and percentage sign, then convert to float
            text_value = change_percent_element.text.replace('(', '').replace(')', '').replace('%', '')
            stock_data["regular_market_change_percent"] = float(text_value) / 100 if text_value else None
        except:
            print(f"Could not find regular market change percent using selector: {change_percent_selector}")

        # Get post-market price
        post_price_selector = "[data-testid='qsp-post-price']"
        try:
            post_price_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, post_price_selector))
            )
            post_price_text = post_price_element.text.replace(',', '') # Remove commas
            stock_data["post_market_price"] = float(post_price_text)
        except:
            print(f"Could not find post-market price using selector: {post_price_selector}")

        # Get post-market change
        post_change_selector = "[data-testid='qsp-post-price-change']"
        try:
            post_change_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, post_change_selector))
            )
            # Remove the '+' sign if present before converting to float
            text_value = post_change_element.text.lstrip('+')
            stock_data["post_market_change"] = float(text_value)
        except:
            print(f"Could not find post-market change using selector: {post_change_selector}")

        # Get post-market change percent
        post_change_percent_selector = "[data-testid='qsp-post-price-change-percent']"
        try:
            post_change_percent_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, post_change_percent_selector))
            )
            # Remove parentheses, percentage sign, and '+' sign, then convert to float
            text_value = post_change_percent_element.text.replace('(', '').replace(')', '').replace('%', '').lstrip('+')
            stock_data["post_market_change_percent"] = float(text_value) / 100 if text_value else None
        except:
            print(f"Could not find post-market change percent using selector: {post_change_percent_selector}")

        return stock_data

    except Exception as e:
        print(f"An error occurred while fetching data for {symbol}: {e}")
        return stock_data

    finally:
        if 'driver' in locals() and driver:
            driver.quit()

# Test program to test web scraping functions
def main():
    # stock_symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "META", "NVDA", "NFLX", "JNJ", "JPM"]
    stock_symbols = ["AAPL", "GOOGL"]
    stock_symbols.sort()

    print("Fetching stock prices...")
    for symbol in stock_symbols:
        price = get_stock_price(symbol)
        if price:
            print(f"{symbol}: ${price}")
        else:
            print(f"{symbol}: Price not found")

    print("Fetching stock data...")
    for symbol in stock_symbols:
        data = get_stock_data(symbol)
        if data:
            print(f"{symbol}: ${data}")
        else:
            print(f"{symbol}: Data not found")
        print("")

# execute only if run as a script
if __name__ == "__main__":
    main()
