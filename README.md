# josbot v0.6
A Twitter / Mastodon bot that posts random quotes from a TXT file. 

Currently used to post lines from the play *De Jossen* by Tom Lanoye. Live on [@dejossen](http://twitter.com/dejossen) and [@dejossen@mastodon-belgium.be](https://mastodon-belgium.be/@dejossen). One could easily use this bot to post other content, by replacing the lines provided in `quotes.txt`. The code is general and well documented.

## Text
The full play got manually restructured to 426 lines of each 140 characters max, starting from the [original text](https://github.com/Forceflow/josbot/raw/main/De-Jossen.-Val-en-revival-der-saamhorigheid.pdf) which was released publicly on 2014 on Tom Lanoye's website. Tried to keep consistency when splitting lines in multiple posts, so there's never a split mid-sentence.

## Requirements
Written for Python 3. Required libraries: 
 * [Tweepy](http://www.tweepy.org/) for Twitter API interaction.
 * [Mastodon.py](https://mastodonpy.readthedocs.io) for Mastodon API interaction.
 * [YAML](http://www.yaml.org/) for reading/writing the settings file. 

How to get these:
 * Ubuntu/Debian: `sudo apt-get install python3 python3-tweepy python3-yaml python3-mastodon`
 * Using pip3: `pip3 install tweepy pyaml Mastodon.py`

## Setup & running
Run ``python3 josbot.py``

If no ``settings.yml`` is found, it will be created in the same directory as ``josbot.py``. This file is used for auth details and program settings.

After configuring ``settings.yml``, run ``python3 josbot.py`` again to start the bot.

The following options are available
 * ``TWITTER_ACCESS_KEY``, ``TWITTER_ACCESS_SECRET``, ``TWITTER_CONSUMER_KEY`` and ``TWITTER_CONSUMER_SECRET``: Auth configuration for Twitter, using the [Oauth 1.0a (User Context)](https://developer.twitter.com/en/docs/tutorials/authenticating-with-twitter-api-for-enterprise/authentication-method-overview#oauth1.0a) method.
 * ``MASTODON_TOKEN`` and ``MASTODON_BASE_URL``: Auth configuration for Mastodon. Base URL is the instance that hosts the account you want to post to (for example: ``https://mastodon.social/``).
 * ``dry_run_mastodon`` and ``dry_run_twitter``: If you want to test the bot without actually posting to Twitter or Mastodon (a "dry run"), set this to ``true``. The time between posts will be reduced and the bot will print out the fake calls to output.
 * ``followback_twitter``: Try to follow back all followers on Twitter (due to API changes this is finicky. Runs in a seperate thread.)
 * ``followback_mastodon``: Try to follow back all followers on Mastodon. Currently **not implemented**.
 * ``line_index``: The current line of quotes.txt you're posting. This allows the bot to resume after a system reboot without starting all over again.

 If the bot reaches the end of quotes.txt, the file is shuffled and the process starts over.

## Rights
From the original PDF:

> De tekst van De Jossen. Val en revival der saamhorigheid mag vrij worden gedownload en verspreid.
> Opvoeringen, geheel of gedeeltelijk, mogen pas plaatsvinden na een voorafgaande schriftelijke afspraak
> met SABAM

I'm assuming running Josbot is not a *rendition* but a *distribution* of the source material, which is explicitly allowed.

## Todo

* Single-post and exit mode
* Configurable settings file location
