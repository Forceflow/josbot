# JosBot v0.7
# Author: @jbaert

VERSION="0.7"

# standard python libs
import random, time, sys, os.path, io, threading
# additional libs (get these from your OS repositories or pip)
import yaml, tweepy
from mastodon import Mastodon

# prefixes for logging
PREFIX="Josbot   :"
PREFIX_TW="Twitter  :"
PREFIX_MA="Mastodon :"

# CONFIG
SLEEPMIN = 86400 # At least 24 hrs between tweets (60*60*24)
SLEEPMAX = 172800 # At max 48 hrs between tweets (60*60*48)

# GLOBALS
settings_file = "settings.yml"
lines_file = "lines.txt"
settings = {}
lines = {}

# Function to go to sleep for a random period between SLEEPMIN and SLEEPMAX
def sleeploop():
	# Pick random sleeptime
	sleeptime = random.randint(SLEEPMIN,SLEEPMAX)
	# Print sleeptime in human readable form
	m, s = divmod(sleeptime, 60) # An alternate syntax when dealing with multiple return values is to have Python "unwrap" the tuple 
	h, m = divmod(m, 60)
	print(PREFIX, "Going to sleep for %d:%02d:%02d" % (h, m, s))
	# Do the sleeps
	time.sleep(sleeptime)

# Setup Mastodon auth
def setupMastodonAuth():
	print(PREFIX_MA, "Setting up Mastodon auth")
	mastodon_api = Mastodon(access_token = settings['MASTODON_TOKEN'], api_base_url = settings['MASTODON_BASE_URL'])
	return mastodon_api

# Post a line to Mastodon
def tootLine(api, line):
	print(PREFIX_MA, "Tooting")
	api.status_post(line)

# Setup tweepy twitter auth, return api object
def setupTwitterAuth():
	print(PREFIX_TW, "Setting up Twitter auth")
	auth = tweepy.OAuthHandler(settings['TWITTER_CONSUMER_KEY'], settings['TWITTER_CONSUMER_SECRET'])
	auth.set_access_token(settings['TWITTER_ACCESS_KEY'],settings['TWITTER_ACCESS_SECRET'])
	api = tweepy.API(auth, wait_on_rate_limit=True)
	return api

# Tweet a line
def tweetLine(api, line):
	print(PREFIX_TW, "Tweeting")
	api.update_status(line)

# Manage the TwitterFollowBackThread: start it when it's not running
def manageTwitterFollowBackThread(api, thread):
	if not thread.is_alive():
			print(PREFIX_TW, "Launching FollowbackThread")
			thread.start()
	else:
			print(PREFIX_TW, "FollowbackThread already running")

# Follow all our followers back (threaded)
def twitterFollowBackThread(api):
	print(PREFIX_TW, "Followback Thread: Following all our followers")
	count = 0
	for follower in tweepy.Cursor(api.get_followers).items():
		try:
			print(PREFIX_TW, "Followback Thread: Trying to follow", follower.screen_name)
			follower.follow()
			count += 1
		except tweepy.errors.TweepyException as e:
			# print(PREFIX_TW, "Followback Thread:", e)
			print(PREFIX_TW, "Followback Thread: Hit a limit during following, sleeping for 20mins")
			time.sleep(60*60)
	print(PREFIX_TW, "Followback Thread: Finished: Followed", count, "accounts")

# Write a sample config
def writeSampleConfig(filename):
	settings = {
	"TWITTER_CONSUMER_KEY":"KEYHERE",
	"TWITTER_CONSUMER_SECRET":"SECRETHERE",
	"TWITTER_ACCESS_KEY":"KEYHERE",
	"TWITTER_ACCESS_SECRET":"SECRETHERE",
	"MASTODON_TOKEN":"TOKENHERE",
	"MASTODON_BASE_URL": "https://MASTODON_INSTANCE_URL_HERE/",
	"dry_run_twitter": False,
	"dry_run_mastodon": False,
	"followback_twitter": False,
	"followback_mastodon": False,
	"loop:": True,
	"loop_shuffle": True,
	"line_index":0
	}
	yaml.dump(settings, open(filename, "w"), default_flow_style=False)

# Load settings from file (if fail: write sample config and quit)
def loadSettings():
	if os.path.exists(settings_file):
		global settings
		settings = yaml.safe_load(open(settings_file, "r"))
		print(PREFIX, "Loaded", len(settings), "settings from", settings_file)
	else:
		writeSampleConfig(settings_file)
		print(PREFIX, "No settings file found - wrote a sample config to ", settings_file)
		print(PREFIX, "Provide the required settings and re-run the program.")
		quit()

# Save settings to file
def saveSettings():
	yaml.dump(settings, open(settings_file, "w"), default_flow_style=False)

# Load and sanitize quotes from utf-8 txt file
def loadLines():
	with io.open(lines_file, mode="r", encoding="utf-8") as f:
		content = [line.rstrip('\n').strip()[0:140] for line in f]
	global lines
	lines = content
	print(PREFIX, "Loaded", str(len(content)), "lines from", lines_file)

# Shuffle quotes and write them back to file
def shuffleLines():
	random.shuffle(lines)
	file = io.open(lines_file, mode="w", encoding="utf-8")
	file.truncate(0)
	for line in lines:
		file.write("%s\n" % line)

# MAIN PROGRAM LOOP
def main():
	print(PREFIX, "Version", VERSION, "starting")
	
	# Load settings and lines
	loadSettings()
	loadLines()

	# Check if we're doing a dry run
	if settings["dry_run_twitter"]:
		print(PREFIX_TW, "Dry run, not really posting to Twitter. FOR TESTING PURPOSES.")
	if settings["dry_run_mastodon"]:
		print(PREFIX_MA, "Dry run, not really posting to Mastodon. FOR TESTING PURPOSES.")
	
	# Setup Twitter AUTH and FOLLOWBACK THREAD
	twitter_api = "NULL"
	if not settings["dry_run_twitter"]:
		twitter_api = setupTwitterAuth()
		if settings["followback_twitter"]:
			twitter_followback_thread = threading.Thread(target=twitterFollowBackThread, args=(twitter_api,))

	# Setup Mastodon AUTH
	mastodon_api = "NULL"
	if not settings["dry_run_mastodon"]:
		mastodon_api = setupMastodonAuth()

	print(PREFIX, "End of setup")
	# MAIN LOOP
	print(PREFIX, "-------------------------------")
	print(PREFIX, "Starting main loop")
	while True:
		if int(settings["line_index"]) < len(lines):
			# SLEEP (skip if we're in a dry run)
			if settings["dry_run_twitter"] and settings["dry_run_mastodon"]:
				time.sleep(0.2)
			else:
				sleeploop()

			# GET CURRENT QUOTE
			current_index=int(settings["line_index"])
			current_line=lines[current_index]
			print(PREFIX, "Current line:", current_line, "[", current_index,"]")

			# TWEET
			if not settings["dry_run_twitter"]:
				tweetLine(twitter_api, current_line)
			else:
				print(PREFIX_TW, "(DRY RUN) Tweeting")
			
			# TOOT
			if not settings["dry_run_mastodon"]:
				tootLine(mastodon_api, current_line)
			else:
				print(PREFIX_MA, "(DRY RUN) Tooting")

			# INCREMENT QUOTE INDEX
			settings["line_index"] = current_index + 1
			saveSettings()

			# MANAGE TWITTER FOLLOWBACK THREAD
			if not settings["dry_run_twitter"] and settings["followback_twitter"]:
				manageTwitterFollowBackThread(twitter_api, twitter_followback_thread)

		else:
			print(PREFIX, "Ran out of lines")
			if not settings["loop"]:
				print(PREFIX, "Looping is set to false, so exiting")
				quit()
			if(settings["loop_shuffle"]):
				print(PREFIX, "Shuffling lines before restarting")
				shuffleLines()
			settings["line_index"] = 0
			saveSettings()
			print(PREFIX, "Restarting loop")
if __name__ == "__main__": main()
