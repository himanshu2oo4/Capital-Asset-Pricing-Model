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

def app():
    st.title("Calculate Risk  and Return")

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
        fig = px.bar(return_df, x='Stock', y='Return Value', title='Expected return for Stocks',color_discrete_sequence=random_colors)
        fig.update_traces(texttemplate='%{y}%', textposition='inside')
        st.plotly_chart(fig , use_container_width=True)
        
    # further new addons : -------
        
    #     if st.button("Wanna buy some stock > ? " ):
    #         st.text('Different webistes from which you can buy stocks for you.. 💹💸')
    # # Redirect using HTML
    #         st.markdown(
    #             """
    #             <style>
    #                 .centered {
    #                 display: flex;
    #                 flex-direction: column;
    #                 align-items: center;
    #                 justify-content: center;
    #                 height: 100vh;  /* 100% of the viewport height */
    #             }
    #                 a {
    #                     text-decoration: none;
    #                     color: inherit;
    #                 }
    #             </style>
    #             <a href="https://groww.in/" class = 'centered' target="_blank">On Grow</a>
    #             <a href="https://upstox.com/" class = 'centered' target="_blank">On Upstox</a>
    #             <a href="" target="_blank" class = 'centered'>On Upstox</a>
    #             <a href="https://www.5paisa.com/" class = 'centered' target="_blank">On 5Paisa</a>
    #             <a href="https://zerodha.com/" class = 'centered' target="_blank">On Zerodha</a>          
    #             """,
    #             unsafe_allow_html=True
    #         )
        
        st.markdown(
                """
                <style>
                    .centered {
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content: center;
                        height: 100vh;  /* 100% of the viewport height */
                    }
                </style>
                """,
                unsafe_allow_html=True
            )

# Centered container for the button and messages
        with st.container() as centered_container:
                if st.button("Wanna buy some stock?"):
                    st.text('Different websites from which you can buy stocks for you.. 💹💸')

                    # Redirect using HTML
                    st.markdown(
                        """
                        <a href="https://groww.in/" class='centered' target="_blank">On Grow</a>
                        <a href="https://upstox.com/" class='centered' target="_blank">On Upstox</a>
                        <a href="" class='centered' target="_blank">On Some Website</a>
                        <a href="https://www.5paisa.com/" class='centered' target="_blank">On 5Paisa</a>
                        <a href="https://zerodha.com/" class='centered' target="_blank">On Zerodha</a>
                        """,
                        unsafe_allow_html=True
                    )

            # Set the container to be centered
        centered_container.set_styled()
    









    except:
        st.error("Error Occurred! Please try again.")