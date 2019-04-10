import tweepy
from textblob import TextBlob
import re

# Tweepy - Twitter Authentication
consumer_key = 'ozmnBDLlM16DTIlfAjv66JFwj'
consumer_secret = 'D9LVuLFY0rr4Gsyt37WY0GuHQlAoJFNDp4vktZwXT1S62ry3XC'

access_token = '419961622-q92J6hPrnJzmE0l5uvivCop9R0yobLyRFyOXicQm'
access_token_secret = '2Y7QrwMQ63Yu8d2IWTkIsB56ujT4ohg21r6EfXpt8NHLf'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Query - Parameters and inputs

# List of candidates of the 2020 Democratic Party presidential primaries
democratic_candidates = ['Cory Booker', 'Pete Buttigieg', 'Julian Castro', 'John Delaney', 'Tulsi Gabbard',
                         'Kirsten Gillibrand', 'Mike Gravel', 'Kamala Harris', 'John Hickenlooper', 'Jay Inslee',
                         'Amy Klobuchar', 'Wayne Messam', "Beto O'Rourke", 'Tim Ryan', 'Bernie Sanders',
                         'Eric Swalwell', 'Elizabeth Warren', 'Marianne Williamson', 'Andrew Yang']
# Hashtag relevant to the topic. Will eventually include debate hashtags.
relevant_hashtag = '2020Election'


# Clean tweet using regex so the tweet is placed into the CSV file
def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


# Label whether the polarity is negative, neutral, or positive
def get_tweet_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'


candidate_polarities = dict()
for candidate in democratic_candidates:
    this_candidate_polarities = []
    # Query tweets regarding election and the candidate themselves.
    candidate_public_tweets = api.search(q=[relevant_hashtag, candidate], count=100)
    # Using regex we will reformat their name to fit filename requirements
    candidate = re.sub('[^A-Za-z0-9]+', '', candidate)
    # Now we will save the tweets in a .csv file in order to display the information better.
    with open('%s_tweets.csv' % candidate, 'w') as this_candidate_file:
        this_candidate_file.write('tweet,sentiment_label\n')
        for tweet in candidate_public_tweets:
            analysis = TextBlob(clean_tweet(tweet.text))
            # Get the label corresponding to the sentiment analysis
            this_candidate_polarities.append(analysis.sentiment[0])
            this_candidate_file.write('%s,%s\n' % (tweet.text.encode('utf8'), get_tweet_sentiment(tweet.text)))
