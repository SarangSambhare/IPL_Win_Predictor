import streamlit as st
import pandas as pd
import pickle
hide = """
<style>
@MainMenu {visibility : hidden;}
  footer {visibility : hidden;}
  </style>
"""
teams =  [
 'Sunrisers Hyderabad', 
 'Mumbai Indians' ,
 'Royal Challengers Bangalore',
 'Kolkata Knight Riders' , 
 'Kings XI Punjab',
 'Chennai Super Kings', 
 'Rajasthan Royals' ,
 'Delhi Capitals'
]
cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
       'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
       'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
       'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
       'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
       'Sharjah', 'Mohali', 'Bengaluru'
]
pipe = pickle.load(open('pipe.pkl','rb'));
st.set_page_config(page_title='Win predictor');
st.title("IPL Win Predictor");
st.markdown(hide,unsafe_allow_html=True)

col1 , col2 = st.columns(2);

with col1:
   batting_team =  st.selectbox("Select The Batting Team",sorted(teams))
with col2:
   bowling_team =st.selectbox("Select the Bowling team",sorted(teams))     

cities = st.selectbox("Select Match city",sorted(cities))
target = st.number_input('Target');

st.text("Enter Current Situation below")


col3,col4,col5 = st.columns(3);
with(col3):
   score = st.number_input("Score")
with(col4):
   overs = st.number_input("Overs")   
with(col5):
   wickets = st.number_input("Wickets out")
if st.button("Predict win probablity"):
  runs_Left = target-score
  balls_left = 120 - (overs*6)
  wickets = 10 - wickets
  crr = score/overs
  rrr = (runs_Left*6)/balls_left
  input_df = pd.DataFrame({'batting_team' : [batting_team],'bowling_team':[bowling_team],'city' : [cities],'runs_left' :[runs_Left],'balls_left' : [balls_left],'wickets' : [wickets],'total_runs_x':[target],'crr':[crr],'rrr':[rrr]})
  result = pipe.predict_proba(input_df)
  loss = result[0][0]
  win = result[0][1]
  st.text(batting_team + " : "+str(round(win*100))+"%");
  st.text(bowling_team + " : "+str(round(loss*100))+"%");