# JosBot v0.5
# Author: @jbaert

VERSION="0.5"

# standard python libs
import random, time, sys, os.path, io, threading
# additional libs (get these from your OS repositories or pip)
import yaml, tweepy

# CONFIG
SLEEPMIN = 86400 # At least 24 hrs between tweets (60*60*24)
SLEEPMAX = 172800 # At max 48 hrs between tweets (60*60*48)

# GLOBALS
settings = {}
settings_file = "settings.yml"
quotes = []
quotes_file = "quotes.txt"

# DISABLE TWEETS
dry_run = False

def main():
	print("Josbot", VERSION, "starting, loading settings from", settings_file)
	# Grab settings from file
	loadSettings(settings_file)
	# Setup AUTH
	if dry_run:
		print("Started in DRY RUN mode: No interaction with Twitter API will be made.")
		api = "NULL"
	else:
		api = setupAuth()
	# Load quotes from file
	global quotes
	quotes = loadQuotes(quotes_file)

	# Prepare followback thread
	followback_thread = threading.Thread(target=threaded_followBack, args=(api,dry_run))

	# Main loop
	print("Starting main loop")
	while True:
		if int(settings["tweetindex"]) < len(quotes):
			# FOLLOWBACK
			if not followback_thread.is_alive():
				followback_thread = threading.Thread(target=threaded_followBack, args=(api,dry_run)) # create new thread
				print("Launching Followback Thread")
				followback_thread.start()
			else:
				print("Followback thread already running")
			# SLEEP
			sleeptime = random.randint(SLEEPMIN,SLEEPMAX)
			m, s = divmod(sleeptime, 60) # An alternate syntax when dealing with multiple return values is to have Python "unwrap" the tuple 
			h, m = divmod(m, 60)
			print("Going to sleep for %d:%02d:%02d" % (h, m, s))
			time.sleep(sleeptime)
			# TWEET
			tweetQuote(api,dry_run)
		else:
			print("Ran out of quotes ... shuffle and restart")
			resetQuotes(quotes_file)
			settings["tweetindex"] = 0
			saveSettings(settings_file)

# Setup tweepy twitter auth, return api object
def setupAuth():
	print("Setting up Twitter auth")
	auth = tweepy.OAuthHandler(settings['CONSUMER_KEY'], settings['CONSUMER_SECRET'])
	auth.set_access_token(settings['ACCESS_KEY'],settings['ACCESS_SECRET'])
	api = tweepy.API(auth, wait_on_rate_limit=True)
	return api

# Load settings from file (if fail: write sample config)
def loadSettings(filename):
	if os.path.exists(filename):
		global settings
		settings = yaml.load(open(filename, "r"), Loader=yaml.BaseLoader)
		print("Settings loaded")
	else:
		writeSampleConfig(filename)
		print("No settings file found - wrote a sample config to ", filename)
		print("Provide the required settings and re-run the program.")
		quit()

# Tweet a quote given by tweetindex in settings to a certain api
def tweetQuote(api, dry_run):
	# grab tweetindex as int
	tweet_index=int(settings["tweetindex"])
	# tweet the quote
	if not dry_run:
		print("Tweeting quote", tweet_index, ":", quotes[tweet_index])
		api.update_status(quotes[tweet_index])
	else:
		print("DRY RUN: Not really tweeting quote ", tweet_index, " : ", quotes[tweet_index])
	# increment tweet_index and persist in settings
	settings["tweetindex"] = tweet_index + 1
	saveSettings(settings_file)

# Follow all our followers back (threaded)
def threaded_followBack(api, dry_run):
	if(dry_run):
		print("(FOLLOWBACK_THREAD) DRY RUN: Following all followers")
		return
	else:
		print("(FOLLOWBACK_THREAD) Following all our followers")
	# Actual follow code
	count = 0
	for follower in tweepy.Cursor(api.followers).items():
		try:
			# print("(FOLLOWBACK_THREAD) Trying to follow", follower.screen_name)
			follower.follow()
			count += 1
		except tweepy.TweepError:
			print("(FOLLOWBACK_THREAD) Hit a limit during following, sleeping for 20mins")
			time.sleep(60*60)
	print("(FOLLOWBACK_THREAD) FINISHED: Followed", count, "people")
			
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
	with io.open(filename, mode="r", encoding="utf-8") as f:
		content = [line.rstrip('\n').strip()[0:140] for line in f]
	print("Loaded", str(len(content)), "quotes from", quotes_file)
	return content

# Shuffle quotes and write them back to file
def resetQuotes(filename):
	random.shuffle(quotes)
	file = io.open(filename, mode="w", encoding="utf-8")
	file.truncate(0)
	for quote in quotes:
		file.write("%s\n" % quote)

if __name__ == "__main__": main()
