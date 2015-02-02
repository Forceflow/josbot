import tweepy, time, sys, pickle, os.path, json


# GLOBALS
execfile('credentials.py')

def main():
	print "Josbot starting..."
	tweet_index = importTweetIndex()
	api = setupAuth()

def setupAuth():
	print "Setting up Twitter auth"
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
  	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth)
	return api

# To remember which quote we last tweeted, the bot persists its last tweet index to a JSON file
# This allows us to easy add new quotes to the quotes.txt
# Returns the last quote that was tweeted index
def importTweetIndex():
	print "Importing tweet index"
	tweet_index = [0]
	if os.path.exists("tweetindex.txt"):
		tweet_index = json.load(open("tweetindex.txt", "r"))
	else:
		json.dump(tweet_index, open("tweetindex.txt", "w"))
	print "Current tweet index: " + str(tweet_index)
	return tweet_index;
		
#def readquotes():
#	api.
	
	


if __name__ == "__main__": main()

