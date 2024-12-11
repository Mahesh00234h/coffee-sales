import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error


try:
    data = pd.read_csv("index.csv", parse_dates=["date", "datetime"])
    st.success("Dataset loaded successfully!")
except FileNotFoundError:
    st.error("Error: Dataset file not found.")
    st.stop()


st.title("Coffee Sales Analysis Dashboard")



st.header("1. Exploratory Data Analysis (EDA)")


daily_sales = data.groupby('date')['money'].sum()


st.subheader("Total Daily Coffee Sales")
fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.lineplot(x=daily_sales.index, y=daily_sales.values, ax=ax1)
ax1.set_title("Total Daily Coffee Sales")
ax1.set_xlabel("Date")
ax1.set_ylabel("Sales (Money)")
ax1.tick_params(axis='x', rotation=45)
ax1.grid()
st.pyplot(fig1)


st.subheader("Coffee Popularity by Type")
coffee_popularity = data['coffee_name'].value_counts()
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(x=coffee_popularity.index, y=coffee_popularity.values, ax=ax2, palette="viridis")
ax2.set_title("Coffee Popularity by Type")
ax2.set_xlabel("Coffee Name")
ax2.set_ylabel("Number of Orders")
ax2.tick_params(axis='x', rotation=45)
st.pyplot(fig2)


st.subheader("Payment Method Breakdown")
payment_methods = data['cash_type'].value_counts()
fig3, ax3 = plt.subplots(figsize=(7, 7))
ax3.pie(payment_methods, labels=payment_methods.index, autopct='%1.1f%%', startangle=90, colors=["gold", "lightblue"])
ax3.set_title("Payment Method Breakdown")
st.pyplot(fig3)



st.header("2. Sales Forecasting")


sales_data = daily_sales.reset_index()
sales_data.set_index('date', inplace=True)

train = sales_data[:-30]
test = sales_data[-30:]


try:
    model = ARIMA(train['money'], order=(5, 1, 0))  
    model_fit = model.fit()
    st.success("ARIMA model fitted successfully!")
except Exception as e:
    st.error(f"Error fitting ARIMA model: {e}")
    st.stop()


forecast = model_fit.forecast(steps=30)
test['forecast'] = forecast.values


st.subheader("Sales Forecast")
fig4, ax4 = plt.subplots(figsize=(12, 6))
ax4.plot(train['money'], label="Training Data")
ax4.plot(test['money'], label="Test Data")
ax4.plot(test['forecast'], label="Forecast", linestyle='--')
ax4.legend()
ax4.set_title("Sales Forecast")
ax4.set_xlabel("Date")
ax4.set_ylabel("Sales (Money)")
ax4.grid()
st.pyplot(fig4)


mse = mean_squared_error(test['money'], test['forecast'])
st.write(f"Mean Squared Error: {mse:.2f}")



st.header("3. Specific Customer Purchases")


st.subheader("Top 5 Customers by Purchase Frequency")
top_customers = data['card'].value_counts().head(5)
fig5, ax5 = plt.subplots(figsize=(8, 5))
sns.barplot(x=top_customers.index, y=top_customers.values, ax=ax5, palette="coolwarm")
ax5.set_title("Top 5 Customers by Purchase Frequency")
ax5.set_xlabel("Customer ID")
ax5.set_ylabel("Number of Transactions")
st.pyplot(fig5)


customer_id = st.text_input("Enter Customer ID to analyze (e.g., ANON-0000-0000-0002):")
if customer_id:
    if customer_id in data['card'].values:
        customer_data = data[data['card'] == customer_id]

        st.write("Customer's Purchase Summary:")
        customer_summary = customer_data.groupby('coffee_name')['money'].sum()
        st.dataframe(customer_summary)

      
        fig6, ax6 = plt.subplots(figsize=(10, 5))
        sns.barplot(x=customer_summary.index, y=customer_summary.values, ax=ax6, palette="magma")
        ax6.set_title(f"Purchases by Customer {customer_id}")
        ax6.set_xlabel("Coffee Name")
        ax6.set_ylabel("Total Money Spent")
        ax6.tick_params(axis='x', rotation=45)
        st.pyplot(fig6)
    else:
        st.error("Customer ID not found.")
