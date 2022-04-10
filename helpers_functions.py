def mark_negative_words(neg_words, tokenized_sentence):
    # create the HTML code and mark the negative words red in a sentence
    result = ""
    marked = False
    for word in tokenized_sentence:
        space = " "
        if not(word.isalnum()):
            # if the word is not an alphabetic letter, do not add a space
            space = ""
        if word in neg_words:
            # mark the negative word red (in HTML code)
            word = "<span style=\"color: #ff0000\">" + word + "</span>"
            marked = True
        result += space + word
    result = result.strip()
    return result, marked


def make_class_prob(class_prob):
    # create the code for the class probability
    result = ""
    result += "<div class=\"certainty_wrapper\">"
    result += "<div id=\"inside\">"
    result += "<div class=\"percentage\">"
    result += "Certainty: " + str(class_prob) + "%"
    result += "</div> </div>"
    result += "<div class=\"circle\">"
    result += "<div class=\"line\">"
    result += "</div>"
    result += "<div class=\"bar right\">"
    result += "<div class=\"certainty\"></div>"
    result += "</div>" + "</div>" + "</div>"
    return result


def make_reviewed_buttons(cyberbully):
    # make the buttons for tweets that are reviewed
    result = ""
    if cyberbully:
        # if the class is cyberbully make 2 buttons: rephrase button and post anyways button
        result += "<form>\n"
        result += "<a href=# id=rephrase class=\"rephrase_button\"><button>Rephrase Tweet</button></a>\n"
        result += "</form>\n"
        result += "<form>\n"
        result += "<a href=# id=post_anyways class=\"post_anyways\"><button>Post Anyways</button></a>\n"
        result += "</form>\n"
        return result
    else:
        # if the class is not cyberbully make just 1 button
        result += "<form>\n"
        result += "<a href=# id=tweet><button>Post My Tweet!</button></a>\n"
        result += "</form>\n"


def make_review_tweet(tweet, pred, neg_words, class_prob):
    # make the result after pressing the "review tweet" button
    result = ""
    result += "<h1>Your tweet was: \'" + tweet + "\'</h1>\n"
    cyberbully = False
    if pred != "Not Cyberbullying":
        cyberbully = True
        result += "<h1>Warning you are discriminating based on " + pred + "</h1>\n"
        if len(neg_words) != 0:
            result += "<h1>Please delete, or rephrase the red words</h1>\n"
        else:
            result += "<h1>Please rephrase your Tweet</h1>"
    else:
        result += "<h1>No Cyberbullying was detected!</h1>"
    # make the buttons HTML code
    buttons = make_reviewed_buttons(cyberbully)
    # make the class probabilities HTML code
    class_prob = make_class_prob(class_prob)
    return result, buttons, class_prob