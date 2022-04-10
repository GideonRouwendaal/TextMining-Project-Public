print("Importing libraries")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Parameters
save = True
show = False
#import csv file
print("Reading file")
file = pd.read_csv('cyberbullying_tweets(good).csv')
df = pd.DataFrame(file)

#count instances of each class
classes = df['cyberbullying_type'].value_counts()
classes = pd.DataFrame(classes)

#barplot instances of each class
fig = plt.figure(figsize=(12,5))
plt.bar(classes.index, classes['cyberbullying_type'], color='#1da1f2')
plt.xlabel('Classes')
plt.ylabel('Data isntances')
plt.title('Data spread')
if show == True:
    plt.show()
if save == True:
    fig.savefig("Class_Distribution.png")
    print("Saved class distribution")


#calculate length of each tweet
print("Calculating tweet length")
tweet_length = []
for i in range(len(df)):
    length = len(df['tweet_text'].iloc[i])
    if length > 500:
        print(df['tweet_text'].iloc[i])
        print("++++++++++++++++++++++++++++")
    tweet_length.append(length)
    

average_length = np.mean(tweet_length)
df['tweet_length']= tweet_length

#histogram for tweet legnths
print("Plotting tweet length")
fig2=plt.figure(figsize=(10,5))
plt.hist(df['tweet_length'], bins=[0,100,200,300,400], color='#1da1f2')
plt.xlabel('Number of characters')
plt.ylabel('Data instances')
plt.title('Histogram: Tweet Length')
if show == True:
    plt.show()
if save == True:
    fig2.savefig("Tweet_Length_Distribution.png")
    print("Saved tweet length distribution")