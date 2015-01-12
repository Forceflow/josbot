import tweepy, time, sys

# Init twitter credentials
execfile('credentials.py')

def main():
	print "Josbot starting..."
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
  	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth)

def readquotes():
	
	


if __name__ == "__main__": main()

