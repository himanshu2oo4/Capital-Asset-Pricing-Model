from dotenv import load_dotenv
load_dotenv()
import streamlit as st 
import os 
import google.generativeai as genai 
from PIL import Image
import bs4 as bs 
import requests
import datetime 
import pandas as pd 
import pandas_datareader.data as web
import yfinance as yf 

import webbrowser
def app():
    
    st.header('CAPITAL MIND AI ')
    html = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = bs.BeautifulSoup(html.text)

    tickers = []

    table = soup.find('table',{"class": "wikitable sortable"})
    rows = table.findAll('tr')[1:]
    for row in rows:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker[:-1])
    
    
    stocks_list = st.multiselect("**Choose stocks**", (tickers),(tickers[0]))

    year = 1 
    
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
    except Exception as e:
        print(f'Exception occured : {e}') 

    stock_data = stocks_df.to_string()

    genai.configure(api_key = os.getenv('Google_api_key'))
    # func to load gemini pro model 

    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history = [])

    def get_gemini_response(question):
        prompt = f"your name is CAPITAL MIND AI and your owner and master is HIMANSHU, you act as a stock Analyst ,Equity research analyst , financial advisor , bank investors, i provided you the data of diff stocks do a comparative analyis of {stock_data} generate a clear and short answer in 50 words to my question based on the analysis. my question is {question}"
        response = chat.send_message(prompt , stream = True)
        return response


    col1 , col2 = st.columns(2)
    with col1 : 
        st.subheader('Capital Mind : Text Chat')

        if 'chat_history' not in st.session_state:
            st.session_state['chat_history']= []

        input = st.text_input('Input : ', key = 'input')
        submit = st.button('Ask the question ')

        if submit and input :
            response = get_gemini_response(input)
            # add user query and response to session chat history 

            st.session_state['chat_history'].append(('**You**' , input))
            st.subheader('The Response :-')
            response.resolve()
            st.write(response.text)
            # for chunk in response:
            #     st.write(chunk.text , end= '')
            # st.write(response.text)
            st.session_state['chat_history'].append(('**Capital Mind**', response.text))
        st.subheader('chat history :-')
        for role , text in st.session_state['chat_history']:
            st.write(f'{role} : {text}')
    with col2 : 
        st.subheader('Capital Mind : Image chat')
        inputt = st.text_input('Input : ' , key = 'inputt')
        prompt = f"your name is CAPITAL MIND AI and your owner and master is HIMANSHU, you act as a stock Analyst ,Equity research analyst , financial advisor , bank investors, i provided you a image and do a comparative analysis and use your all powers to generate a clear and crisp answer in 50 tokens to my question based on the analysis , my question is {inputt}" 
        model = genai.GenerativeModel('gemini-pro-vision')

        def get_gemini_response(prompt ,image):
            response = model.generate_content([prompt, image])
            return response.text


        uploaded_file  = st.file_uploader('choose an image' , type = ['jpg' , 'jpeg' , 'png'])
        image = ''
        if uploaded_file!= None : 
            image = Image.open(uploaded_file)
            st.image(image , caption= 'Uploaded image', use_column_width= True)
        submit = st.button('Lets work on the image')
        if submit : 
            response = get_gemini_response(prompt , image)
            st.subheader('Response is : ')
            st.write(response,use_column_width= True)



