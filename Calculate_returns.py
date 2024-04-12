import streamlit as st
import bs4 as bs
import requests
import numpy as np
import pandas as pd
import datetime
import pandas_datareader.data as web
import yfinance as yf 
import plotly.express as px 
import CAPM_Functions
import random
import seaborn as sns 
import webbrowser
import os 
from dotenv import load_dotenv
def app():
    st.header("Calculate Risk  and Return")

    st.write("Assuming the Benchmark used in Market Returns:")
    st.markdown("- if beta = 0 this means the stock is uncorrelated to the market")
    st.markdown("- if beta = 1 this means the stock is perfectly correlated to the market and this implies the stock has the same volatality as the market")
    st.markdown("- if beta > 1 this means the stock is more volatile than the market")
    st.markdown("- if beta < 1 this means the stock is less volatile than the market")

    #web scrapping data for user input
    html = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = bs.BeautifulSoup(html.text)

    tickers = []

    table = soup.find('table',{"class": "wikitable sortable"})
    rows = table.findAll('tr')[1:]
    for row in rows:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker[:-1])


    #user inputs
    col1,col2 = st.columns([1,1])
    with col1:
        stocks_list = st.multiselect("**Choose stocks**", (tickers),(tickers[0]))

    with col2:
        year = st.number_input("**Number of years**",1,10)
    
    #function to calculate daily returns
    def daily_returns(df):
        df_daily_return = df.copy()
        for i in df.columns[1:]:
            for j in range(1,len(df)):
                df_daily_return[i][j] = ((df[i][j]-df[i][j-1])/df[i][j-1])*100
            df_daily_return[i][0]=0
        return df_daily_return
    
    # ------- New Addings ------------
    try:
        end = datetime.date.today()
        start = datetime.date(datetime.date.today().year-year, datetime.date.today().month, datetime.date.today().day)

        SP500 = web.DataReader(["sp500"],"fred",start,end)
        #print(SP500.head())


        stocks_df = pd.DataFrame()

        for stock in stocks_list:
            data = yf.download(stock, period=f"{year}y")
            stocks_df[f'{stock}'] = data['Close']


        stocks_df.reset_index(inplace=True)
        SP500.reset_index(inplace=True)
        SP500.columns = ["Date", "sp500"]

        stocks_df = pd.merge(stocks_df,SP500, on="Date", how="inner")

        stocks_daily_return = CAPM_Functions.daily_returns(stocks_df)

        beta = {}
        alpha = {}

        for i in stocks_daily_return.columns:
            if i != 'Date' and i != "sp500":
                b,a = CAPM_Functions.calculate_beta(stocks_daily_return,i)
        
                beta[i] = b
                alpha[i] = a

        beta_df = pd.DataFrame(columns=["Stock","Beta Value", "Risk Factor"])
        beta_df["Stock"] = beta.keys()
        beta_df["Beta Value"] = [round(i,2) for i in beta.values()]
        beta_df['Risk Factor'] = ['low risk' if i <= 1 else 'high risk' for i in beta_df['Beta Value']]


        with col1:
            st.markdown("### Calculated Beta Value (Risk)")
            st.dataframe(beta_df, use_container_width=True)

        rf=0
        rm=stocks_daily_return["sp500"].mean()*252

        return_df = pd.DataFrame()
        return_value = []

        for stock, value in beta.items():
            return_value.append(str(round(rf+(value*(rm-rf)),2)))
        return_df["Stock"] = stocks_list
        return_df["Return Value"] = return_value

        with col2:
            st.markdown("### Calculated Expected Return using CAPM")
            st.dataframe(return_df, use_container_width=True)
       
        random_colors = ['#%06x' % random.randint(0, 0xFFFFFF) for _ in range(len(return_df))]


        with st.container():
            st.write("----")
            st.markdown('### Expected Increase in price')
            fig = px.bar(return_df, x='Stock', y='Return Value',color_discrete_sequence=random_colors)
            fig.update_traces(texttemplate='%{y:.2f}', textposition='inside')
            st.plotly_chart(fig , use_container_width=True)
            




        
        
    # further new addons : -------

        def get_risk_free_rate():
        # Use the yield on a 1-year Treasury bill as a proxy for the risk-free rate
            rsSymbol = "^IRX"
            risk_free_data = yf.download(rsSymbol, start=start, end=end)
            risk_free_rate = risk_free_data['Close'].iloc[-1] / 100  # Convert percentage to decimal
            return risk_free_rate
        def calculate_expected_return(stock_data, risk_free_rate, market_return):
            expected_returns = []

            for stock_symbol in stock_data.columns:
                    stock_returns = stock_data[stock_symbol].pct_change().dropna()
                    import statsmodels.api as sm
                    # Calculate beta using linear regression
                    market_returns = yf.download("^GSPC", start=start, end=end)['Adj Close'].pct_change().dropna()
                    X = sm.add_constant(market_returns)
                    model = sm.OLS(stock_returns, X).fit()
                    beta = model.params['Adj Close']
                    print(beta)
                    # Calculate expected return using CAPM
                    expected_return = risk_free_rate + beta * (market_return - risk_free_rate)
                    expected_returns.append((stock_symbol, expected_return))

            return expected_returns
        # Download ADJ Close data of stocks 
        stocks_data = pd.DataFrame()
        for stock_symbol in stocks_list:
            data = yf.download(stock_symbol, start=start, end=end)
            stocks_data[f'{stock_symbol}'] = data['Adj Close']

        # Calculate expected return using CAPM
        risk_free_rate = get_risk_free_rate()
        market_return = yf.download("^GSPC", start=start, end=end)['Adj Close'].pct_change().mean()
        expected_returns = calculate_expected_return(stocks_data , risk_free_rate, market_return)


        expected_returns_df = pd.DataFrame(expected_returns, columns=['Stock', 'Expected Return'])
        RandomColors = ['#%06x' % random.randint(0, 0xFFFFFF) for _ in range(len(expected_returns_df))]
        # st.dataframe(expected_returns_df)
        st.markdown('### Overall Expected Return (%) wrt Market return value')
        fig = px.bar(expected_returns_df, x='Stock', y='Expected Return',color_discrete_sequence=RandomColors)
        fig.update_traces(texttemplate='%{y:.2f}%', textposition='inside')
        st.plotly_chart(fig , use_container_width=True)
        




        


        # st.markdown('''
        # <a href="https://groww.in/" target="_blank">
        # <button type="button">On grow</button>
        # </a> 
        # <a href="https://upstox.com/" target="_blank">
        # <button type="button">On upstox</button>
        # </a>   
        # <a href="https://5paisa.com/" target="_blank">
        # <button type="button">On 5paisa</button>
        # </a>   
        # <a href="https://Zerodha.com/" target="_blank">
        # <button type="button">On Zerodha</button>
        # </a>     


        # ''' , unsafe_allow_html = True)

        # new -----------
        st.markdown('''
    <div style="display: flex; justify-content: space-around;">
        <h3>Wanna buy any of these stocks 💹💸 ? </h3> <br>
        <a href="https://groww.in/" target="_blank">
            <button type="button">On Groww</button>
        </a> 
        <a href="https://upstox.com/" target="_blank">
            <button type="button">On Upstox</button>
        </a>   
        <a href="https://5paisa.com/" target="_blank">
            <button type="button">On 5paisa</button>
        </a>   
        <a href="https://zerodha.com/" target="_blank">
            <button type="button">On Zerodha</button>
        </a>
    </div>
''', unsafe_allow_html=True)
        buttoncss = """
        <style>
        h3{
        text-align:center ;
        
        }
        button {
    padding: 10px 20px;
    font-size: 16px;
    background-color: #69DE96; # back color 
    color: #fff; /* White text color */
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease-in-out;
    display : block ;
    margin : auto ;
    margin-top : 20px ; 
}

/* Hover effect */
button:hover {
    background-color: #000000; /* Darker blue color on hover */
    color : #fff ; 
    transform: scale(1.1);
}        
</style>
""" 
        st.markdown(buttoncss , unsafe_allow_html=True)


        load_dotenv()
        key = os.getenv('Google_api_key')

        # print(table)



    

    except:
        st.error("Error Occurred! Please try again.")

    