import numpy as np
import streamlit as st
import datetime
import yfinance as yf
import plotly.express as px
from neuralprophet import NeuralProphet

from utils import *
import login

# Initialize SQL connection.
# Uses @st.cache_resource to run only once
@st.cache_resource
def init_conn():
    db_url = st.secrets["DATABASE_URL"]
    return st.connection("postgresql", type="sql", url=db_url)
conn = init_conn()

# Get the email of the user
email = login.email_fn()

try:
    # Run SQL query to get the login status of the user
    login_status = conn.query(f"SELECT login_status FROM users WHERE email = '{email}';", ttl="10m")
    login_status = login_status.iloc[0, 0]

    if login_status == 'TRUE':
        # Get the name of the user
        name = login.name_fn()

        # Add options
        option = st.sidebar.selectbox(
        f'Hi, {name}',
        ("Settings",),
        index=None,
        placeholder="Menu",
        )

        # Display a message with the bot icon
        st.title("Welcome to Stock Trend App 💹")
        st.write("This is a simple Streamlit app to forecast the stock close price.")

        # Get ticker symbol from user
        tickerSymbol = st.sidebar.text_input('Enter Stock Ticker')

        # Display a date input widget
        start_date = st.sidebar.date_input("Select Start Date", min_value=datetime.date(2000, 1, 1), max_value=datetime.date.today(), value=datetime.date(2012, 1, 1))
        end_date = st.sidebar.date_input("Select End Date", min_value=datetime.date(2000, 1, 1), max_value=datetime.date.today(), value=datetime.date.today())

        # Get number of days to forecast
        future_days = st.sidebar.number_input("Enter Days to Forecast", min_value=1, value=100, step=1)

        button = st.sidebar.button("Submit")

        if button:
            if not tickerSymbol:
                st.write("Please enter a valid Stock Ticker")
            elif start_date > end_date:
                st.write("Please enter valid dates. Start Date cannot exceed the End Date.")
            else:
                
                    # Get data on this ticker
                    tickerData = yf.Ticker(tickerSymbol)

                    # Get the historical prices for this ticker
                    df = tickerData.history(period='1d', start=start_date, end=end_date)
                    df = df.reset_index()

                    # Get company information
                    company_name = tickerData.info['longName']
                    st.sidebar.write(f"Company Name: {company_name}")

                    # describing data
                    st.subheader(f'Data from {start_date} to {end_date}')
                    st.write(df.describe())

                    # Visualization
                    st.subheader(f'{tickerSymbol.upper()} Close Price vs Time')
                    st.line_chart(df, x="Date", y="Close", color="#0514C0")
                    
                    stock = df[['Date', 'Close']]

                    # the NeuralProphet model expects the input DataFrame to have two columns: 'ds' (datetime) and 'y' (target variable).
                    stock.columns = ['ds', 'y']

                    # Train the model
                    NP_model = NeuralProphet()
                    NP_model.fit(stock)

                    # Evaluate the model
                    future = NP_model.make_future_dataframe(stock, periods=future_days)

                    prediction = NP_model.predict(stock)
                    forecast = NP_model.predict(future)
                    
                    # Plot the future forecast
                    st.subheader(f'{future_days} Days Forecasting')
                    fig3 = px.line(forecast, x="ds", y="yhat1", color_discrete_sequence=['red'])
                    fig3.update_layout(xaxis_title='Day', yaxis_title='Close Price')
                    # Plot!
                    st.plotly_chart(fig3, use_container_width=True)
                    
                    st.subheader("Components of Forecast")
                    fig_components = NP_model.plot_components(forecast)
                    st.plotly_chart(fig_components)

                    # Calculate the trend component of the forecast
                    trend = forecast['trend'].values

                    # Calculate the change in trend
                    trend_change = np.diff(trend)

                    # Check if the trend is positive, negative, or flat
                    if all(change > 0 for change in trend_change):
                        trend_status = "Sell"
                    elif all(change < 0 for change in trend_change):
                        trend_status = "Buy"
                    else:
                        trend_status = "Hold"

                    # Display a bot icon and the trend status to the right side of the icon
                    st.write(f"<div style='display: flex; align-items: center;'>"
                                f"<p style='font-size: 48px;'>🤖</p>"
                                f"<div style='margin-left: 20px; font-size: 24px; font-weight: bold;'>{trend_status}</div>"
                                f"</div>", unsafe_allow_html=True)
                    

        # Actions to perfom when user select an option
        if option == "Settings":
            # Redirect to profile management page
            st.switch_page('pages/profile.py')

except IndexError:
    st.error("Unauthorized Access. Please Login")
    st.switch_page('index.py')