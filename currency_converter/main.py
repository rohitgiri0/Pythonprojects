
# live currency calculator

import streamlit as st
import requests

# Currency info with names
currencies = {
    "USD": "US Dollar",
    "EUR": "Euro",
    "GBP": "British Pound Sterling",
    "INR": "Indian Rupee",
    "JPY": "Japanese Yen",
    "AUD": "Australian Dollar",
    "CAD": "Canadian Dollar",
    "CHF": "Swiss Franc",
    "CNY": "Chinese Yuan",
    "HKD": "Hong Kong Dollar",
    "SGD": "Singapore Dollar",
    "NZD": "New Zealand Dollar",
    "ZAR": "South African Rand",
    "SEK": "Swedish Krona",
    "NOK": "Norwegian Krone",
    "DKK": "Danish Krone",
    "AED": "UAE Dirham",
    "SAR": "Saudi Riyal",
    "RUB": "Russian Ruble",
    "KRW": "South Korean Won"
}

# Create dropdown options like "USD - US Dollar"
currency_options = [f"{code} - {name}" for code, name in currencies.items()]

st.title("💱 Live Currency Converter")
st.subheader("A web app for converting currencies in real-time")
st.sidebar.write("login via name to Continue")
name = st.sidebar.text_input("Enter your name")
if name:
    name = name.capitalize()
    st.sidebar.write(f"Welcome, {name}!")
    

    amt = st.number_input("Enter the amount", min_value=1.0)

    col1, col2 = st.columns(2)

    with col1:
        base_display = st.selectbox("Select your base currency", currency_options, index=3)
        base_currency = base_display.split(" - ")[0]
        st.write(f"Base currency: `{base_currency}`")

    with col2:
        target_display = st.selectbox("Pick the target currency", currency_options, index=0)
        target_currency = target_display.split(" - ")[0]
        st.write(f"Converting to: `{target_currency}`")

    if st.button("Convert"):
        key = "b8afd10e3b201fef7ad5613b"
        url = f"https://v6.exchangerate-api.com/v6/{key}/latest/{base_currency}"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            rate = data["conversion_rates"].get(target_currency)

            if rate:
                converted = rate * amt
                st.subheader(f"{amt} {base_currency} = {converted:.2f} {target_currency}")
                st.success("✅ Conversion successful!")
            else:
                st.error("❌ Target currency not found in API response.")
        else:
            st.error("❌ Failed to fetch data from API.")
