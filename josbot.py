# JosBot v0.4 - Started on 2015/02/04
# Author: @jbaert

# standard libs
import random, time, sys, os.path, io
# additional libs
import yaml, tweepy

# CONFIG
SLEEPMIN = 86400 # At least 24 hrs between tweets (60*60*24)
SLEEPMAX = 172800 # At max 48 hrs between tweets (60*60*48)

# GLOBALS
settings = {}
quotes = []

# DISABLE TWEETS
dry_run = False

# Main program loop
def main():
	print("Josbot starting")
	loadSettings("settings.yml")
	if dry_run:
		print("Started in DRY RUN mode: No interaction with Twitter API will be made.")
		api = "NULL"
	else:
		api = setupAuth()
	global quotes
	quotes = loadQuotes("quotes.txt")

	print("Starting main loop")
	while True:
		if int(settings["tweetindex"]) < len(quotes):
			followBack(api, dry_run)
			# SLEEP until next quote
			sleeptime = random.randint(SLEEPMIN,SLEEPMAX)
			m, s = divmod(sleeptime, 60) # An alternate syntax when dealing with multiple return values is to have Python "unwrap" the tuple 
			h, m = divmod(m, 60)
			print("Going to sleep for %d:%02d:%02d" % (h, m, s))
			time.sleep(sleeptime)
			# TWEET quote
			tweetQuote(api,dry_run)
			# Follow all our followers back
			followBack(api, dry_run)
		else:
			print("Ran out of quotes ... shuffle and restart")
			resetQuotes("quotes.txt")
			settings["tweetindex"] = 0
			saveSettings("settings.yml")

# Setup tweepy twitter auth, return api object
def setupAuth():
	print("Setting up Twitter auth")
	auth = tweepy.OAuthHandler(settings['CONSUMER_KEY'], settings['CONSUMER_SECRET'])
	auth.set_access_token(settings['ACCESS_KEY'],settings['ACCESS_SECRET'])
	api = tweepy.API(auth, wait_on_rate_limit=True)
	return api

# Load settings from file (if fail: write sample config)
def loadSettings(filename):
	if os.path.exists("settings.yml"):
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
		print("Tweeting quote ", tweet_index, " : ", quotes[tweet_index])
		api.update_status(quotes[tweet_index])
	else:
		print("DRY RUN: Not really tweeting quote ", tweet_index, " : ", quotes[tweet_index])
	# increment tweet_index and persist in settings
	settings["tweetindex"] = tweet_index + 1
	saveSettings("settings.yml")

# Follow all our followers back
# TODO: rework this - I think the Tweepy friendship API changed again
def followBack(api, dry_run):
	if(dry_run):
		print("DRY RUN: Follwing all followers")
		return
	else:
		print("Following all our followers")
	count = 0
	for follower in tweepy.Cursor(api.followers).items():
		time.sleep(30)
		try:
			follower.follow()
		except tweepy.TweepError:
			print("Can't follow more today, will try back later")
			break
		count += 1
	print("You now follow", count, "people")
			
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
	print("Loaded", str(len(content)), "quotes")
	return content

# Shuffle quotes and write them back to file
def resetQuotes(filename):
	random.shuffle(quotes)
	file = io.open(filename, mode="w", encoding="utf-8")
	file.truncate(0)
	for quote in quotes:
		file.write("%s\n" % quote)

if __name__ == "__main__": main()