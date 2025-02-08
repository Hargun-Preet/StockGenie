import streamlit as st
import requests

def fetch_stock_news(query):
    api_key = '505ae098a3844233b7b585a955e8a6cb'
    url = f'https://newsapi.org/v2/everything?q={query}&apiKey={api_key}'
    response = requests.get(url)
    data = response.json()
    return data['articles']

def stock_news_page():
    st.title("Stock Market News")
    keyword = st.text_input("Enter a keyword to filter news", value="stocks")
    
    if keyword:
        news_articles = fetch_stock_news(keyword)

        if news_articles:
            for article in news_articles:
                st.markdown(f"### [{article['title']}]({article['url']})")
                st.write(article['description'])
                st.write(f"Published at: {article['publishedAt']}")
                st.write("---")
        else:
            st.write("No news articles found.")
