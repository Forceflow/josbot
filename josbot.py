# JosBot v0.2 - Started on 2015/02/04
# Author: @jbaert

# standard libs
import random, time, sys, os.path, codecs
# additional libs
import yaml, tweepy

# GLOBALS
settings = {}
quotes = []

# Main program loop
def main():
	print "Josbot starting..."
	loadSettings("settings.yml")
	api = setupAuth()
	global quotes
	quotes = loadQuotes("quotes.txt")

	print "Starting main loop ..."
	while settings["tweetindex"] < len(quotes):
		# Sleeptime until next quote
		sleeptime = random.randint(21600,86400)
		m, s = divmod(sleeptime, 60)
		h, m = divmod(m, 60)
		print "Going to sleep for %d:%02d:%02d" % (h, m, s) 
		time.sleep(sleeptime)
		# Tweet it
		tweetQuote(api)
		# Persist new settings (the tweetindex)
		saveSettings("settings.yml")
		# Follow all our followers back
		followBack(api)

	print "Ran out of quotes ... exiting"

# Setup tweepy twitter auth, return api object
def setupAuth():
	print "Setting up Twitter auth"
	auth = tweepy.OAuthHandler(settings['CONSUMER_KEY'], settings['CONSUMER_SECRET'])
  	auth.set_access_token(settings['ACCESS_KEY'], settings['ACCESS_SECRET'])
	api = tweepy.API(auth)
	return api

# Load settings from file (if fail: write sample config)
def loadSettings(filename):
	if os.path.exists("settings.yml"):
		global settings
		settings = yaml.load(open(filename, "r"))
		print "Settings loaded"
		
	else:
		writeSampleConfig(filename)
		print "No settings file found - wrote a sample config to "+filename
		print "Provide the required settings and re-run the program."
		quit()

# Tweet a quote given by tweetindex in settings to a certain api
def tweetQuote(api):
	print "Tweeting quote "+ str(settings["tweetindex"]) + " : "+ quotes[settings["tweetindex"]]
	api.update_status(quotes[settings["tweetindex"]])
	settings["tweetindex"] = settings["tweetindex"] + 1

# Follow all our followers back
def followBack(api):
	print "Following all our followers ..."
	for follower in tweepy.Cursor(api.followers).items():
		follower.follow()

# Save settings to file
def saveSettings(filename):
	yaml.dump(settings, open(filename, "w"), default_flow_style=False)
		
# Write a sample config
def writeSampleConfig(filename):
	settings = { 
	"CONSUMER_KEY":"KEYHERE",
	"CONSUMER_SECRET":"SECRETHERE",
	"ACCESS_KEY":"KEYHERE",
	"ACCESS_SECRET":"SECRETHERE",
	"tweetindex":0
	}
	yaml.dump(settings, open(filename, "w"), default_flow_style=False)
	
# Load and sanitize quotes from utf-8 txt file
def loadQuotes(filename):
	with codecs.open(filename,'r','utf-8') as f:
    		content = [line.rstrip('\n').strip()[0:140] for line in f]
	print "Loaded " + str(len(content)) + " quotes"
	return content


if __name__ == "__main__": main()
