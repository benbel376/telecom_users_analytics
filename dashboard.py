import pandas as pd
import numpy
import streamlit as st
import os
import pickle
from sklearn.preprocessing import StandardScaler
from PIL import Image
# setting path to file and folders
user_df= pd.read_csv("./data/teleco_user_sat_data.csv")

st.title("What is your customer's satisfaction level?")
st.subheader("This model will predict the satisfaction score of a user")

model = pickle.load(open("./models/pridict_satisfaction_model.sav", 'rb'))
#result = loaded_model.score(x_test, y_test)
#result

xdr = st.number_input("xDr_session_count")
tot = st.number_input("Total Data Volume")
dur = st.number_input("Total Session Duration")
rtt = st.number_input("Average RTT")
tp = st.number_input("Average Throughput")
tcp = st.number_input("TCP volume")

input_data = [xdr , tot, dur , rtt, tp, tcp]
prediction = model.predict([input_data])

st.subheader("The satisfaction score is: {}".format ( prediction))

st.subheader("The Dataset")

st.write(
  user_df
)


image = Image.open('./applications.jpg')

st.image(image, caption='scatter plot of applications and total data volume')