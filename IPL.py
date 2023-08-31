import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import pickle
match = pd.read_csv('matches.csv')
delivery = pd.read_csv('deliveries.csv')

total_score_d = delivery.groupby(['match_id','inning']).sum()['total_runs'].reset_index()

total_score_df = total_score_d[total_score_d['inning']==1]

match_df = match.merge(total_score_df[['match_id','total_runs']],left_on='id',right_on = 'match_id')

team = [
 'Sunrisers Hyderabad', 
 'Mumbai Indians' ,
 'Royal Challengers Bangalore',
 'Kolkata Knight Riders' , 
 'Kings XI Punjab',
 'Chennai Super Kings', 
 'Rajasthan Royals' ,
 'Delhi Capitals'
]

match_df['team1'] = match_df['team1'].str.replace('Delhi Daredevils','Delhi Capitals')
match_df['team2'] = match_df['team2'].str.replace('Delhi Daredevils','Delhi Capitals')

match_df['team1'] = match_df['team1'].str.replace('Deccan Chargers','Sunrisers Hyderabad')
match_df['team2'] = match_df['team2'].str.replace('Deccan Chargers','Sunrisers Hyderabad')

match_df = match_df[match_df['team1'].isin(team)]
match_df = match_df[match_df['team2'].isin(team)]

match_df = match_df[match_df['dl_applied']==0]

match_df = match_df[['match_id','city','winner','total_runs']]

delivery_df = match_df.merge(delivery,on='match_id');
delivery_df = delivery_df[delivery_df['inning']==2]

delivery_df['current_score'] = delivery_df.groupby('match_id')['total_runs_y'].cumsum()
delivery_df['runs_left'] = delivery_df['total_runs_x']+1 - delivery_df['current_score']
delivery_df['balls_left'] = 126-(delivery_df['over']*6 + delivery_df['ball'])

delivery_df['player_dismissed'] = delivery_df['player_dismissed'].fillna('0');
delivery_df['player_dismissed'] = delivery_df['player_dismissed'].apply(lambda x:x if x=="0" else "1")
delivery_df['player_dismissed'] = delivery_df['player_dismissed'].astype("int");
wickets = delivery_df.groupby('match_id')['player_dismissed'].cumsum();
delivery_df['wickets'] = 10 - wickets

delivery_df['crr'] = delivery_df['current_score']*6/(120-delivery_df['balls_left'])
delivery_df['rrr'] = (delivery_df['runs_left']*6)/delivery_df['balls_left']

def result(row):
    return 1 if row['batting_team'] == row['winner'] else 0
delivery_df['result']=delivery_df.apply(result,axis=1);

final_df = delivery_df[['batting_team','bowling_team','city','runs_left','balls_left','wickets','total_runs_x','crr','rrr','result']]
final_df=final_df.sample(final_df.shape[0])
final_df.dropna(inplace=True)
final_df = final_df[final_df['balls_left']!=0]
X = final_df.iloc[:,:-1]
y = final_df.iloc[:,-1]
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=1)

trf = ColumnTransformer([
    ('trf',OneHotEncoder(sparse = False,drop = 'first'),['batting_team','bowling_team','city'])
]
  ,remainder='passthrough')

pipe = Pipeline(steps=[
    ('step1',trf),
    ('steo2',LogisticRegression(solver='liblinear'))
])
pipe.fit(X_train,y_train)


y_pred = pipe.predict(X_test)
print(accuracy_score(y_test,y_pred))
pickle.dump(pipe,open("pipe.pkl",'wb'))
