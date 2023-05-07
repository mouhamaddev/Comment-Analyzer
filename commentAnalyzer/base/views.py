from django.shortcuts import render
# Import necessary libraries
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob


# Create your views here.
def CommentAnalyzer(request, my_comment):
    # set of stop words to be removed from the comments
    stop_words = set(stopwords.words('english'))
    # word lemmatizer to normalize the words
    lemmatizer = WordNetLemmatizer()

    # function to preprocess the comments
    def preprocess_comment(comment):
        # tokenize and lowercase the comment
        words = word_tokenize(comment.lower())
        # remove stop words from the comment
        words = [word for word in words if word not in stop_words]
        # normalize words in the comment
        words = [lemmatizer.lemmatize(word) for word in words]
        # join the words back into a string
        comment = ' '.join(words)
        return comment
    
    # function to convert sentiment to rating
    def sentiment_to_rating(sentiment):
        if sentiment > 0:
            return 5
        elif sentiment == 0:
            return 3
        else:
            return 1

    # list of comments to analyze
    comments = [my_comment]
    # preprocess the comments
    preprocessed_comments = [preprocess_comment(comment) for comment in comments]
    # calculate sentiment polarity for each comment using TextBlob
    sentiments = [TextBlob(comment).sentiment.polarity for comment in preprocessed_comments]
    # convert sentiment polarity to rating using sentiment_to_rating function
    ratings_predicted = [sentiment_to_rating(sentiment) for sentiment in sentiments]
    # return the predicted ratings as a JSON response
    response_data = {"ratings": ratings_predicted}
    return JsonResponse(response_data, safe=False)