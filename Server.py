#To setup:
# set FLASK_APP=Server
#For dev:
# set FLASK_ENV=development
#To run:
# flask run
from flask import Flask, request, render_template, jsonify
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from tweet_sentiment_analyzer import vader_analysis_tweet
import json
import numpy as np
from transformers import pipeline
from helpers_functions import mark_negative_words, make_review_tweet

app = Flask(__name__)
#Homepage route
@app.route('/')
def index():
    #Load index html
    return render_template("index.html")

#Process input tweet and return prediction
@app.route('/review_tweet', methods=['POST'])
def process_tweet():
    #Define transformer path
    model_path = 'Models/Transformer'
    #The labels
    labels = ['age','ethnicity','gender','Not Cyberbullying','other type of cyberbullying','religion']
    #Init VADER model
    vader_model = SentimentIntensityAnalyzer()
    #Fetch the tweet
    tweet = request.form.get("tweet")
    # Save the original tweet in order to determine its length in javascript
    org_tweet = tweet
    # Get the negative words of the tweet
    _, negative_words, tokenized_sentence = vader_analysis_tweet(vader_model, tweet)
    #Load the model pipeline
    pipe = pipeline('text-classification',model_path, return_all_scores=True, device = 0)
    #Get the model predictions, returns a list with label and probability. As the model has a max of 128 tokens, cut the rest.
    if len(tweet) > 128:
        tweet = tweet[:128]
        pred = np.asarray(pipe(tweet))
    else:
        pred = np.asarray(pipe(tweet))
    #Get only probabilites in their own list
    predictions = []
    for i in range(pred.shape[1]):
        score = pred[0][i]['score']
        predictions.append(score)
    #Create a numpy array from the predictions
    all_classes_prediction = np.asarray(predictions)
    #Get highest certainty value as a percentage
    class_prob = round(np.amax(all_classes_prediction)*100,2)
    class_prob_percentage = str(class_prob) + "%"
    #Get the class that was predicted, returns a index
    predicted_class = all_classes_prediction.argmax(axis=-1)
    #Get the label by index, using the predicted class position
    pred = labels[predicted_class]
    # mark the negative words in the tweet if not cyberbullying
    if pred == "Not Cyberbullying":
        marked_tweet = tweet
    else:
        marked_tweet, _ = mark_negative_words(negative_words, tokenized_sentence)
    #Temp store data in case tweet needs to be published (globals don't work in flask)
    temp_tweet ={
        "tweet" : tweet,
        "pred_class": pred,
        "prob" : class_prob,
        "tweet_html_code" : marked_tweet
    }
    #store the tweet in cache
    with open("db/cache.json", "w") as temp_db:
        json.dump(temp_tweet, temp_db)
    #Return the tweet and the prediction
    reviewed_tweet, buttons, class_prob_html = make_review_tweet(marked_tweet, pred, negative_words, class_prob)
    return json.dumps({'reviewed_tweet' : reviewed_tweet,'buttons' : buttons, 'class_prob_html' : class_prob_html, 'org_tweet' : org_tweet, 'class_prob' : class_prob_percentage})

#Post the tweet
@app.route('/post_tweet')
def save_tweet():
    #Open the real DB
    with open("db/database.json") as db_r:
      tweet_db = json.load(db_r)
    #Open the cached tweet json
    try:
        with open("db/cache.json") as temp_db_r:
          temp_tweet = json.load(temp_db_r)
        # Prepend the cache values to the real db
        tweet_db.insert(0, {
            "tweet": temp_tweet['tweet'],
            "pred_class": temp_tweet['pred_class'],
            "prob": temp_tweet['prob'],
            "tweet_html_code": temp_tweet['tweet_html_code']
        })
        # Save the newly created JSON
        with open("db/database.json", 'w') as db_w:
            json.dump(tweet_db, db_w,
                      indent=3,
                      separators=(',', ': '))
    except:
        print("No cached tweets found")
    #Close the cache
    open('db/cache.json', 'w').close()
    #Open DB again
    with open("db/database.json", 'r') as db_r:
      tweet_db = json.load(db_r)
    print('Saved to db')
    #Return the newly opened db
    return jsonify(results = tweet_db)

#Load the tweet
@app.route('/load_tweet_db')
def load_tweet():
    #Open DB
    with open("db/database.json", 'r') as db_r:
      tweet_db = json.load(db_r)
    #return db
    return jsonify(results = tweet_db)

#Process the rephrase tweet
@app.route('/rephrase_tweet')
def rephrase_tweet():
    #Open the temp JSON file
    with open("db/cache.json") as temp_db_r:
      temp_tweet = json.load(temp_db_r)
    open('db/cache.json', 'w').close()
    #return the cache
    return jsonify(results = temp_tweet)

if __name__ == '__main__':
    app.run(debug = False)