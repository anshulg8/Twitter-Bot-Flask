from flask import Flask
from flask_basicauth import BasicAuth
from lib import Creds
import tweepy, random, json

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = Creds.USERNAME
app.config['BASIC_AUTH_PASSWORD'] = Creds.PASSWORD
basic_auth = BasicAuth(app)

auth = tweepy.OAuthHandler(Creds.CONSUMER_KEY, Creds.CONSUMER_SECRET)
auth.set_access_token(Creds.ACCESS_KEY, Creds.ACCESS_SECRET)
api = tweepy.API(auth)

@app.route("/")
def home():
    return "Hello World!"

@app.route('/<profile>')
@basic_auth.required
def index(profile):
    if profile in ["motivational"]:
        return post_tweet(f'./data/{profile}.json')
    else:
        return "Invalid Route! Better luck next time.."

def post_tweet(file_name):
    tweet_data = get_quote(file_name)
    if (len(tweet_data) > 280):
        pass
    else:
        print("posting tweet...")
        try:
            if api.update_status(tweet_data):
                return 'success'
        except tweepy.error.TweepError as e:
            return e.reason

def get_quote(file_name):
    f = open(file_name)
    data = json.load(f)
    data_size = len(data['quotes'])
    rand = random.randrange(1,data_size)
    random_quote = data['quotes'][rand]
    tweet = random_quote['quote'] + random_quote['author']
    f.close()
    return tweet

if __name__ == "__main__":
    app.run(debug=True)

# pip3 install -r requirements.txt