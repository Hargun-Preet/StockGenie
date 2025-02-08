import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from keras.models import load_model
import streamlit as st
from auth import login_page, register_page, update_profile
from admin import admin_dashboard
from news import stock_news_page
from covert_currency import currency_conversion_page
from db import register_user, login_user
from sklearn.preprocessing import MinMaxScaler
from streamlit_option_menu import option_menu

# Initialize session state for authentication
if "user" not in st.session_state:
    st.session_state["user"] = None

# Custom CSS for general button styling
st.markdown("""
    <style>
    /* General Logout button styling */
    .stButton > button {
        background-color: #0073e6;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        font-size: 16px;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: #005bb5;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar for navigation using streamlit-option-menu
with st.sidebar:
    if st.session_state["user"]:
        # Hide login/register when logged in and show Stock Prediction and Admin Dashboard options
        nav_options = option_menu(
            menu_title="Navigation",
            options=["Home", "Stock Prediction", "Stock News", "Currency Conversion",  "Update Profile", "Admin Dashboard"] if st.session_state["user"].get("role") == "admin" else ["Home", "Stock Prediction", "Stock News", "Currency Conversion", "Update Profile"],
            icons=["house", "graph-up", "newspaper", "currency-exchange", "person", "shield-lock"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#333333"},  # Dark grey background
                "icon": {"color": "white"},  # White icons
                "nav-link": {"font-size": "16px", "color": "white", "--hover-color": "#678da6"},  # White text with light greyish-blue hover
                "nav-link-selected": {"background-color": "#005bb5", "color": "white"},  # Blue background for active
            }
        )
    else:
        # Show login/register only when not logged in
        nav_options = option_menu(
            menu_title="Navigation",
            options=["Home", "Login", "Register"],
            icons=["house", "box-arrow-in-right", "person-plus"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#333333"},  # Dark grey background
                "icon": {"color": "white"},  # White icons
                "nav-link": {"font-size": "16px", "color": "white", "--hover-color": "#678da6"},  # White text with light greyish-blue hover
                "nav-link-selected": {"background-color": "#005bb5", "color": "white"},  # Blue background for active
            }
        )

# Show Logout button only when logged in
if st.session_state["user"]:
    if st.sidebar.button("Logout"):
        # Safely pop 'user' key without causing error if it's already missing
        st.session_state.pop("user", None)
        st.success("Logged out successfully")

# Stock prediction logic wrapped in a function
def stock_prediction():
    start = '2010-01-01'
    end = '2019-12-31'

    # Use yfinance to download the data
    st.title('Stock Trend Prediction')

    user_input = st.text_input('Enter Stock Ticker', 'AAPL') 

    df = yf.download(user_input, start=start, end=end)

    #Describing Data
    st.subheader('Data from 2010 - 2019')
    st.write(df.describe())

    #Visualisations
    st.subheader('Closing Price v/s Time Chart')
    fig = plt.figure(figsize = (12,6))
    plt.plot(df.Close)
    st.pyplot(fig)


    st.subheader('Closing Price v/s Time Chart with 100MA')
    ma100 = df.Close.rolling(100).mean()
    fig = plt.figure(figsize = (12,6))
    plt.plot(ma100)
    plt.plot(df.Close)
    st.pyplot(fig)


    st.subheader('Closing Price v/s Time Chart with 100MA & 200MA')
    ma100 = df.Close.rolling(100).mean()
    ma200 = df.Close.rolling(200).mean()
    fig = plt.figure(figsize = (12,6))
    plt.plot(ma100)
    plt.plot(ma200)
    plt.plot(df.Close)
    st.pyplot(fig)

    # Splitting Data into Training and Testing

    data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
    data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70): int(len(df))])

    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler(feature_range = (0,1))

    data_training_array = scaler.fit_transform(data_training)

    #Load my model
    model = load_model('keras_model.h5')

    #Testing Part
    past_100_days = data_training.tail(100)

    final_df = pd.concat([past_100_days, data_testing], ignore_index=True)

    input_data = scaler.fit_transform(final_df)

    x_test = []
    y_test = []

    for i in range(100, input_data.shape[0]):
        x_test.append(input_data[i-100: i])
        y_test.append(input_data[i, 0])

    x_test, y_test = np.array(x_test), np.array(y_test)

    # Making predictions

    y_predicted = model.predict(x_test)

    scaler = scaler.scale_

    scale_factor = 1/scaler[0]
    y_predicted = y_predicted * scale_factor
    y_test = y_test * scale_factor

    # Calculate buy/sell signals
    buy_signal_prices = []
    buy_signal_indices = []
    sell_signal_prices = []
    sell_signal_indices = []
    threshold = 0.02  # 2% threshold for significant price movement

    for i in range(1, len(y_predicted)):
        pred_change = (y_predicted[i] - y_predicted[i-1]) / y_predicted[i-1]
    
        if pred_change > threshold:
            buy_signal_indices.append(i)
            buy_signal_prices.append(y_test[i])
        elif pred_change < -threshold:
            sell_signal_indices.append(i)
            sell_signal_prices.append(y_test[i])

    #Final Graph

    st.subheader('Predictions v/s Original')
    fig2 = plt.figure(figsize = (12,6))

    plt.plot(y_test, 'b', label = 'Original Price')
    plt.plot(y_predicted, 'r', label = 'Predicted Price')

    # Plot buy/sell signals
    if buy_signal_indices:
        plt.scatter(buy_signal_indices, buy_signal_prices, color='green', marker='^', 
                label='Buy Signal', alpha=1, s=100)
    if sell_signal_indices:
        plt.scatter(sell_signal_indices, sell_signal_prices, color='red', marker='v', 
                label='Sell Signal', alpha=1, s=100)

    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    st.pyplot(fig2)

    # Display summary of signals
    st.subheader('Trading Signals Summary')
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Buy Signals", len(buy_signal_indices))
    with col2:
        st.metric("Sell Signals", len(sell_signal_indices))

# Initialize session state for authentication
if "user" not in st.session_state:
    st.session_state["user"] = None

# Main page routing logic
if st.session_state["user"]:
    if nav_options == "Stock Prediction":
        stock_prediction()
    elif nav_options == "Stock News":
        stock_news_page()
    elif nav_options == "Currency Conversion":
        currency_conversion_page()
    elif nav_options == "Update Profile":
        update_profile()
    elif nav_options == "Admin Dashboard" and st.session_state["user"].get("role") == "admin":
        admin_dashboard()
    else:
        st.title('Welcome to StockTrendPrediction')

        # Display the image
        st.image('istockphoto-1487894858-612x612.jpg', use_column_width=True)

        # Add subheader and text
        st.subheader('About StockTrendPrediction')
        st.write('StockTrendPrediction is dedicated to empowering investors and traders with the tools they need to make informed financial decisions. Our platform harnesses the power of advanced machine learning algorithms to analyze historical stock data and predict future price movements. We believe that with the right insights, anyone can navigate the complexities of the stock market. Whether you’re a seasoned investor or just starting your trading journey, our user-friendly interface makes it easy to access the information you need.')
        

        st.subheader('Our Mission')
        st.write('At StockTrendPrediction, our mission is to democratize access to financial data and analytics. We aim to provide our users with accurate predictions, intuitive tools, and a supportive community to enhance their investment strategies.')

        # Key Features
        st.write('## Key Features:')
        st.write('- **User-Friendly Interface**: Easy navigation and user experience.')
        st.write('- **Stock Predictions**: Leverage machine learning algorithms to forecast stock movements.')
        st.write('- **Personalized Dashboard**: Access your predictions and manage your profile effortlessly.')

        # Join Us
        st.subheader('Join us to stay ahead in the stock market!')

else:
    if nav_options == "Login":
        login_page()
    elif nav_options == "Register":
        register_page()
    else:
        st.title('Welcome to StockTrendPrediction')

        # Display the image
        st.image('istockphoto-1487894858-612x612.jpg', use_column_width=True)

        # Add subheader and text
        st.subheader('About StockTrendPrediction')
        st.write('StockTrendPrediction is dedicated to empowering investors and traders with the tools they need to make informed financial decisions. Our platform harnesses the power of advanced machine learning algorithms to analyze historical stock data and predict future price movements. We believe that with the right insights, anyone can navigate the complexities of the stock market. Whether you’re a seasoned investor or just starting your trading journey, our user-friendly interface makes it easy to access the information you need.')
        

        st.subheader('Our Mission')
        st.write('At StockTrendPrediction, our mission is to democratize access to financial data and analytics. We aim to provide our users with accurate predictions, intuitive tools, and a supportive community to enhance their investment strategies.')

        # Key Features
        st.write('## Key Features:')
        st.write('- **User-Friendly Interface**: Easy navigation and user experience.')
        st.write('- **Stock Predictions**: Leverage machine learning algorithms to forecast stock movements.')
        st.write('- **Personalized Dashboard**: Access your predictions and manage your profile effortlessly.')

        # Join Us
        st.subheader('Join us to stay ahead in the stock market!')
