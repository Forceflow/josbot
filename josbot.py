# standard libs
import time, sys, os.path
# additional libs
import yaml, tweepy

# GLOBALS
settings = {}

# Main program loop
def main():
	print "Josbot starting..."
	loadSettings("settings.yml")
	api = setupAuth()

# Setup tweepy twitter auth, return api object
def setupAuth():
	print "Setting up Twitter auth"
	auth = tweepy.OAuthHandler(settings['CONSUMER_KEY'], settings['CONSUMER_SECRET'])
  	auth.set_access_token(settings['ACCESS_KEY'], settings['ACCESS_SECRET'])
	api = tweepy.API(auth)
	return api

# Load settings from yaml file (if fail: write sample config)
def loadSettings(filename):
	if os.path.exists("settings.yml"):
		global settings
		settings = yaml.load(open(filename, "r"))
		print "Settings loaded"
		print settings
		
	else:
		writeSampleConfig(filename)
		print "No settings file found - wrote a sample config to "+filename
		print "Provide the required settings and re-run the program."
		quit()

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
	
if __name__ == "__main__": main()
