# currency_conversion_page.py
import streamlit as st
import requests

# Replace with your actual API keys from ExchangeRate-API and NewsAPI
EXCHANGE_API_KEY = 'eedf3296d48ebbb747f139f8'
NEWS_API_KEY = '505ae098a3844233b7b585a955e8a6cb'
BASE_EXCHANGE_URL = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}"
BASE_NEWS_URL = f"https://newsapi.org/v2/everything"

# Currency conversion page function
def currency_conversion_page():
    st.title("Currency Conversion, Exchange Rates, and News")

    # Add currency options
    currency_from = st.selectbox("Convert from", ["USD", "EUR", "GBP", "JPY", "INR", "AUD", "CAD", "CHF", "CNY", "NZD"])
    currency_to = st.selectbox("Convert to", ["USD", "EUR", "GBP", "JPY", "INR", "AUD", "CAD", "CHF", "CNY", "NZD"])

    # Input amount
    amount = st.number_input("Enter amount", min_value=0.0, format="%.2f")

    # Button to convert currency
    if st.button("Convert"):
        if currency_from and currency_to and amount > 0:
            # Make the API request for conversion
            url = f"{BASE_EXCHANGE_URL}/pair/{currency_from}/{currency_to}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                conversion_rate = data['conversion_rate']
                converted_amount = amount * conversion_rate
                st.success(f"{amount} {currency_from} is equal to {converted_amount:.2f} {currency_to}")
                st.write(f"Conversion Rate: 1 {currency_from} = {conversion_rate} {currency_to}")
            else:
                st.error("Error fetching conversion rates. Please check your API key or try again later.")
        else:
            st.error("Please enter valid input.")

    # Button to show exchange rates
    if st.button(f"Show Exchange Rates for {currency_from}"):
        # Fetch exchange rates for the selected currency
        rates_url = f"{BASE_EXCHANGE_URL}/latest/{currency_from}"
        rates_response = requests.get(rates_url)
        if rates_response.status_code == 200:
            rates_data = rates_response.json()
            rates = rates_data['conversion_rates']

            # Display rates
            st.subheader(f"Exchange Rates for {currency_from}")
            for currency, rate in rates.items():
                st.write(f"1 {currency_from} = {rate} {currency}")
        else:
            st.error("Error fetching exchange rates. Please check your API key or try again later.")

    # News section related to the currency
    if st.button(f"Show News for {currency_from}"):
        show_currency_news(currency_from)

# Function to fetch and display news related to the currency
def show_currency_news(currency):
    st.subheader(f"Latest News on {currency}")

    # Define the query to search for news related to the selected currency
    query = f"{currency} currency OR exchange rates OR forex OR trading"

    # Make an API request to fetch the news
    news_url = f"{BASE_NEWS_URL}?q={query}&apiKey={NEWS_API_KEY}"
    news_response = requests.get(news_url)

    if news_response.status_code == 200:
        news_data = news_response.json()
        articles = news_data['articles']

        # Display the top 5 news articles
        if articles:
            for article in articles[:5]:
                st.write(f"### {article['title']}")
                st.write(f"**Source**: {article['source']['name']}")
                st.write(f"{article['description']}")
                st.write(f"[Read more]({article['url']})")
                st.write("---")
        else:
            st.write(f"No recent news articles found for {currency}.")
    else:
        st.error("Error fetching news. Please check your NewsAPI key or try again later.")

