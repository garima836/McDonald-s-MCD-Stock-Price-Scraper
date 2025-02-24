import streamlit as st
import requests
from bs4 import BeautifulSoup
import csv

# Yahoo Finance URL for McDonald's (MCD) stock
stock_symbol = "MCD"
url = f"https://finance.yahoo.com/quote/{stock_symbol}/"

# Headers to mimic a real browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

# Function to fetch stock data
def fetch_stock_data():
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        price_element = soup.find("fin-streamer", {"data-field": "regularMarketPrice"})
        change_element = soup.find("fin-streamer", {"data-field": "regularMarketChange"})
        percent_change_element = soup.find("fin-streamer", {"data-field": "regularMarketChangePercent"})
        price = price_element.text if price_element else "N/A"
        change = change_element.text if change_element else "N/A"
        percent_change = percent_change_element.text if percent_change_element else "N/A"
        return price, change, percent_change
    else:
        st.error(f"Failed to fetch data. Status Code: {response.status_code}")
        return "N/A", "N/A", "N/A"

# Function to save data to CSV
def save_to_csv(data):
    filename = "mcd_stock_data.csv"
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Stock Symbol", "Price", "Change", "Percentage Change"])
        writer.writerow([stock_symbol, *data])
    st.success(f"Data saved to {filename}")

# Streamlit interface
st.title("McDonald's (MCD) Stock Price Scraper")

if st.button("Fetch Stock Data"):
    price, change, percent_change = fetch_stock_data()
    st.write(f"🔹 **Stock:** {stock_symbol}")
    st.write(f"💰 **Price:** ${price}")
    st.write(f"📉 **Change:** {change} ({percent_change}%)")
    save_to_csv((price, change, percent_change))

if __name__ == "__main__":
    fetch_stock_data()
