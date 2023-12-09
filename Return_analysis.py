#importing libraries

import streamlit as st
import requests
import bs4 as bs
import pandas as pd
import yfinance as yf
import datetime
import pandas_datareader.data as web
import CAPM_Functions

def app():

    st.header("S&P 500")
    st.write("The Standard and Poor's 500, or simply the S&P 500, is a stock market index tracking the stock performance of 500 of the largest companies listed on stock exchanges in the United States. It is one of the most commonly followed equity indices.")
    st.write("The S&P 500 stock market index is maintained by S&P Dow Jones Indices. It comprises 503 common stocks which are issued by 500 large-cap companies traded on American stock exchanges (including the 30 companies that compose the Dow Jones Industrial Average). The index includes about 80 percent of the American equity market by capitalization. It is weighted by free-float market capitalization, so more valuable companies account for relatively more weight in the index. The index constituents and the constituent weights are updated regularly using rules published by S&P Dow Jones Indices. Although called the S&P 500, the index contains 503 stocks because it includes two share classes of stock from 3 of its component companies.")
    st.write("[Learn More >](https://en.wikipedia.org/wiki/S%26P_500)")

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
        stocks_list = st.multiselect("**Choose Stocks**", (tickers),(tickers[0]))

    with col2:
        year = st.number_input("**Select the Number of years you want the data for**",1,10)

    #downloading data for SP500(market data)
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

        st.markdown("### Data of Selected Stocks")
        st.dataframe(stocks_df,use_container_width=True)


        col1,col2 = st.columns([1,1])
        with col1:
            st.markdown("### Price of all the Stocks")
            st.plotly_chart(CAPM_Functions.interactive_plot(stocks_df))

        with col2:
            st.markdown("### Price of all the Stocks (After Normalization)")
            st.write("Normalised Indexes — a better way of data visualisation for investment performance comparison")
            st.plotly_chart(CAPM_Functions.interactive_plot(CAPM_Functions.normalize(stocks_df)))
        

        with st.container():
            st.write("----")
            st.header("Why Normalising?")
            st.write("All indexes are calculated based on a reference point of time. For example, Hang Seng Index of Hong Kong stock market takes June 30, 1964 as the reference point. Since the indexes of different stock markets have different referencing points of time, their index levels cannot be compared directly with each other.")
            st.write("For example, the S&P 500 index in the United States today is 4697, while the Hang Seng Index was reported at 25049.")
            st.write("In order to compare their performance over time of different stock market indexes, a normalized index chart is usually plotted. ")

        
        # daily return graph 
        with st.container():
            st.write("----")
            st.markdown('### Daily return of stocks')
            daily_return = CAPM_Functions.daily_returns(stocks_df)

            st.plotly_chart(CAPM_Functions.interactive_plot(daily_return) , use_container_width=True)

    except:
        st.error("Error Occurred! Please try again.")