# 📈 StockGenie – AI-Powered Stock Trend Prediction App

**StockGenie** is a smart and modern stock prediction web app that leverages an LSTM neural network and machine learning to forecast trends and deliver financial insights. Whether you're an investor or an enthusiast, StockGenie makes it easy to analyze stocks, convert currencies, and stay updated with stock-related news — all in one sleek, responsive interface.

## 📹 Demo Video

Click the image below to watch the demo:

[![Watch the video](https://img.youtube.com/vi/hSB1HFjbUyM/0.jpg)](https://youtu.be/hSB1HFjbUyM)

---

## 🚀 Features

- 📊 **Stock Price Prediction** using LSTM deep learning models
- 🗞️ **Stock News Section** with keyword-based filtering
- 💱 **Currency Converter** for real-time forex rates
- 🔐 **User Authentication** (Register/Login with secure JWT)
- 🛠️ **Admin Dashboard** to manage users
- 🧑‍💼 **Profile Update** and **Password Reset**
- 📈 **Interactive Charts** for trend visualization
- 🌐 **Real-time Data** via yFinance and News APIs
- 📱 **Responsive UI** built with Streamlit

---

## 🧰 Tech Stack

- **Frontend/UI:** Streamlit, HTML/CSS
- **Backend:** Python
- **Machine Learning:** TensorFlow, Keras, NumPy, scikit-learn
- **APIs:** yFinance, Currency Exchange API, News API
- **Database:** MongoDB
- **Authentication:** JWT, bcrypt

---

## 🔐 Environment Variables

Create a `.env` file in the root directory and add the following:

```env
MONGO_URI=your_mongodb_uri
JWT_SECRET=your_jwt_secret
EMAIL_USER=your_email@example.com
EMAIL_PASS=your_email_app_password
```

##🛠️ Installation & Setup
1. Clone the Repository
```bash
git clone https://github.com/your-username/StockGenie.git
cd StockGenie
```
2. Set Up Virtual Environment (Recommended)
```bash
python -m venv venv
# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```
3. Install Dependencies
```bash
pip install -r requirements.txt
```
4. Create .env File
Add your credentials to a new .env file in the root directory. See the Environment Variables section above.

5. Run the Application
```bash
streamlit run app.py
```
