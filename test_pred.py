print("Initializing libraries")
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from transformers import pipeline
import numpy as np
import pandas as pd
from alive_progress import alive_bar
import warnings
warnings.filterwarnings('ignore')

#Parameters
training_set_test = False
testing_set_test = True

#Set seeds for reproducability, missing NP and Tensorflow seeds
seed = 1234
#Read the tweets csv file
print("Loading and converting Dataset")
tweets = pd.read_csv("cyberbullying_tweets(good).csv")
#Rename the dataframe columns to label and text, this has to be done for tensorflow to understand where the labels are
tweets = tweets.rename(columns={"cyberbullying_type": "label", "tweet_text": "text"})
#Convert the labels to 0-5
tweets.label = pd.Categorical(tweets.label)
tweets['label'] = tweets.label.cat.codes
print("Loading model")
model_path = 'Models/Transformer'
pipe = pipeline('text-classification',model_path, return_all_scores=True)

#Split the dataset into testing and training sets
print("Splitting data to obtain a train and test set")
tweets_train, tweets_test, labels_train, labels_test = train_test_split(tweets, tweets['label'], test_size=0.2, random_state=seed)

#Get the dataset size
size_dataset_train = tweets_train['label'].shape[0]

if training_set_test == True:
    train_pred = []
    #Initialize the progress bar
    print("Getting predictions on the training set")
    with alive_bar(size_dataset_train, title = "Prediction Progress: ", bar = 'blocks', spinner = 'radioactive') as bar:
        for _, row in tweets_train.iterrows():
            #Set the max score
            max_score = 0.0
            predicted_class = 0
            #Get the prediction of huggingface
            if len(row['text']) > 128:
                text = row['text']
                text = text[:128]
                pred = pipe(text)
            else:
                pred = pipe(row['text'])
            #For everything in the predictions go over it and append the result to the list
            for j in range(len(pred[0])):
                score = pred[0][j]['score']
                if score > max_score:
                    max_score = score
                    predicted_class = j
                else:
                    max_score = max_score
            train_pred.append(predicted_class)
            #Call the progress bar
            bar()
    #Compare the predicted classes with the true classes for the train set
    compared_array_train = np.equal(train_pred, labels_train)
    #Count true and false predictions and print the difference
    true_prediction_count_train = np.count_nonzero(compared_array_train)
    false_prediction_count_train = len(compared_array_train)-true_prediction_count_train
    print("Done calculating on the training set, there were " + str(true_prediction_count_train) + " correct predictions and " + str(false_prediction_count_train) + " incorrect predictions")
    # introduce target names for the classification report
    target_names = ['age','ethnicity','gender','Not Cyberbullying','other type of cyberbullying','religion']
    # classification report
    print(classification_report(labels_train, train_pred, target_names=target_names))

if testing_set_test == True:
    test_pred = []
    ## test set
    size_dataset_test = tweets_test['label'].shape[0]
    #Initialize the progress bar
    print("getting predictions on the test set")
    with alive_bar(size_dataset_test, title = "Prediction Progress: ", bar = 'blocks', spinner = 'radioactive') as bar:
        for _, row in tweets_test.iterrows():
            #Set the max score
            max_score = 0.0
            predicted_class = 0
            #Get the prediction of huggingface
            if len(row['text']) > 128:
                text = row['text']
                text = text[:128]
                pred = pipe(text)
            else:
                pred = pipe(row['text'])
            #For everything in the predictions go over it and append the result to the list
            for j in range(len(pred[0])):
                score = pred[0][j]['score']
                if score > max_score:
                    max_score = score
                    predicted_class = j
                else:
                    max_score = max_score
            test_pred.append(predicted_class)
            #Call the progress bar
            bar()
    #Compare the predicted classes with the true classes for the test set
    compared_array_test = np.equal(test_pred, labels_test)
    #Count true and false predictions and print the difference
    true_prediction_count_test = np.count_nonzero(compared_array_test)
    false_prediction_count_test = len(compared_array_test)-true_prediction_count_test  
    print("Done calculating on the test set, there were " + str(true_prediction_count_test) + " correct predictions and " + str(false_prediction_count_test) + " incorrect predictions")
    # introduce target names for the classification report
    target_names = ['age','ethnicity','gender','Not Cyberbullying','other type of cyberbullying','religion']
    # classification report
    print(classification_report(labels_test, test_pred, target_names=target_names))