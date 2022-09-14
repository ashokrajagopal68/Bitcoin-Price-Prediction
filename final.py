import streamlit as st
import pandas as pd
import sqlite3
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler,StandardScaler
import mpld3
import streamlit.components.v1 as components
from datetime import timedelta, date
import plost

@st.cache(allow_output_mutation=True)
def load_data(db):
    conn = sqlite3.connect(db)
    df = pd.read_sql_query("SELECT * FROM btcprice;", conn)
    conn.close()
    df['date'] = pd.to_datetime(df['date'])
    return df

def load_model(model,weight):
    model_uni = keras.models.load_model(model)
    model_uni.load_weights(weight)
    return model_uni


def create_test_next(test_X, model, window_size = 75, future_days = 30):
    new_test_X = test_X
    for i in range(future_days):
        Last = new_test_X[-1:]
        last2 = Last[0,1:]
        new = np.append(last2,model.predict(new_test_X[-1:]),axis=0)
        #print(new)
        new_test_X = np.append(new_test_X,new.reshape(1,window_size,1),axis=0)
    return new_test_X

df = load_data('btc.db')
model_uni = load_model(model='Univariate_model', weight='uni_weights.h5')

scaler = MinMaxScaler(feature_range=(0,1))
close = np.array(df.iloc[:,5]).reshape(-1,1)
scaler.fit(close)

last75 = np.array(df.iloc[-75:,5]).reshape(-1,1)
last75_sc = scaler.transform(last75)
test_last = np.reshape(last75_sc,(1,75,1))
next_test5 = create_test_next(test_last, model_uni,window_size = 75,future_days = 5)
next_price5 = model_uni.predict(next_test5)
next_5_price = scaler.inverse_transform(next_price5)

st.title("Bitcoin Price Prediction")

st.header("Next 5 days Close Price")

from datetime import date
today = date.today()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric(label = "Today's Close", value ="{price1} $".format(price1=round(next_5_price[0][0])) , delta ="{:.2f} %".format((next_5_price[0][0] - last75[-1][0]) /last75[-1][0]*100 ))
col2.metric(label = "Tomorrow's Close", value ="{price1} $".format(price1=round(next_5_price[1][0])) , delta ="{:.2f} %".format((next_5_price[1][0] - next_5_price[0][0])/next_5_price[0][0]*100 ))
col3.metric(label = today.strftime('%B')+ ' '+str(today.day+2), value ="{price1} $".format(price1=round(next_5_price[2][0])) , delta ="{:.2f} %".format((next_5_price[2][0] - next_5_price[1][0])/next_5_price[1][0]*100 ))
col4.metric(label = today.strftime('%B')+ ' '+str(today.day+3), value ="{price1} $".format(price1=round(next_5_price[3][0])) , delta ="{:.2f} %".format((next_5_price[3][0] - next_5_price[2][0])/next_5_price[2][0]*100 ))
col5.metric(label = today.strftime('%B')+ ' '+str(today.day+4), value ="{price1} $".format(price1=round(next_5_price[4][0])) , delta ="{:.2f} %".format((next_5_price[4][0] - next_5_price[3][0])/next_5_price[3][0]*100 ))

next_d = []
for i in range(5):
    #next_d = []
    x = (date.today() + timedelta(days=i)).strftime('%Y-%m-%d %H:%M:%S')
    next_d.append(x)
next_days = pd.to_datetime(next_d)

tab1, tab2 = st.tabs(["Historic","Prediction"])

with tab1:
    st.header('Historic Price')
    plost.line_chart(data=df, x='date', y='Close', height=500, width=600, pan_zoom='minimap', use_container_width=True)

with tab2:
    st.header('Prediction for next 5 days')
    dates = pd.to_datetime(df['date'])
    fig = plt.figure()
    sns.lineplot(y=df.iloc[-90:,5],x=dates[-90:])
    plt.xlabel('Date')
    plt.ylabel('BTC Price in USD')
    sns.lineplot(x=next_days,y=next_5_price[0:5].reshape(-1))
    plt.legend(['Historic','Predicted'])
    fig_html = mpld3.fig_to_html(fig)
    components.html(fig_html, height=600)


