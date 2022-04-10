print("Importing libraries")
import pandas as pd

#import csv file
print("Reading file")
file = pd.read_csv('cyberbullying_tweets.csv')
df = pd.DataFrame(file)

#seperate wrongly formatted tweets in dataset
print("Removing duplicate tweets")
df2_tweets=[]
df2_type=[]
drop_indexes = []
for i in range(len(df)):
    if '\n' in df['tweet_text'].iloc[i]:
        tweets = df['tweet_text'].iloc[i].split('\n')
        bully_type = df['cyberbullying_type'].iloc[i]
        drop_indexes.append(i)
        for x in tweets:
            df2_tweets.append(x)
            df2_type.append(bully_type)
df= df.drop(drop_indexes, axis=0)
df2 = pd.DataFrame()
df2['tweet_text']=df2_tweets
df2['cyberbullying_type']=df2_type
df3 = pd.concat([df,df2])
df3.to_csv('cyberbullying_tweets(good).csv')
print("Saved cleaned data")