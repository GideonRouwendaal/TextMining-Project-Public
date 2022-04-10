import nltk

def vader_analysis_tweet(vader_model, tweet):
    # tokenize the sentence
    tokenized_sentence = nltk.word_tokenize(tweet)
    neg_word_list = []
    # go over each word
    for word in tokenized_sentence:
        if (vader_model.polarity_scores(word)['compound']) <= -0.1:
            # if the 'compound' of the word <= -0.1, add the word to the negative word list
            neg_word_list.append(word)
    # obtain the polarity score of the tweet
    score = vader_model.polarity_scores(tweet)
    # create a better looking string
    neg_words = ", ".join(neg_word_list)
    return score, neg_words, tokenized_sentence