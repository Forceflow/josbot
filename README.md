# josbot v0.8
A Twitter / Mastodon / Bluesky bot that posts lines from a TXT file.

## Requirements
Written for Python 3. Required libraries: 
 * [Tweepy](http://www.tweepy.org/) for Twitter API interaction.
 * [Mastodon.py](https://mastodonpy.readthedocs.io) for Mastodon API interaction.
 * [atproto](https://pypi.org/project/atproto/) for Bluesky API interaction.
 * [YAML](http://www.yaml.org/) for reading/writing the settings file. 

You can get these using pip3: `pip3 install tweepy pyaml Mastodon.py atproto` (or `pip3 install -r requirements.txt`)

## Setup & running
Run ``python3 josbot.py``

* If no ``settings.yml`` is found, it will be created in the same directory as ``josbot.py``. This file is used for auth details and program settings.
* After configuring ``settings.yml``, run ``python3 josbot.py`` again to start the bot.

The following options are available
 * ``TWITTER_ENABLED``, ``MASTODON_ENABLED``, ``BLUESKY_ENABLED``: Enable / disable individual social networks. When they are all disabled, the bot runs in dry run mode, fake posting a line every 2 seconds.
 * ``TWITTER_ACCESS_KEY``, ``TWITTER_ACCESS_SECRET``, ``TWITTER_CONSUMER_KEY`` and ``TWITTER_CONSUMER_SECRET``: Auth configuration for Twitter, using the [Oauth 1.0a (User Context)](https://developer.twitter.com/en/docs/tutorials/authenticating-with-twitter-api-for-enterprise/authentication-method-overview#oauth1.0a) method.
 * ``MASTODON_TOKEN`` and ``MASTODON_BASE_URL``: Auth configuration for Mastodon. ``MASTODON_BASE_URL`` is the instance that hosts the account you want to post to (for example: ``https://mastodon.social/``).
 * ``BLUESKY_USERNAME`` and ``BLUESKY_PASS``: Bluesky username (only the default BS server is supported atm, so ``YOURNAMEHERE.bsky.social``) and password (or passkey).
 * ``TWITTER_FOLLOWBACK``: Try to follow back all followers on Twitter (due to API changes this is finicky. Runs in a seperate thread.)
 * ``MASTODON_FOLLOWBACK``: Try to follow back all followers on Mastodon. Currently **not implemented**.
 * ``loop``: Start over when the end of the file is reached (default: true)
 * ``loop_shuffle``: Shuffle the lines in the `lines.txt` file when starting over (default: true). This is ignored when ``loop`` is set to false.
 * ``line_index``: The current line of lines.txt you're posting. This allows the bot to resume after a system reboot without starting all over again.

 If the bot reaches the end of `lines.txt`, the file is shuffled and the process starts over.
 
 ## Todo

* Single-post and exit mode
* Configurable wait time between lines
* Configurable settings file location
 
# Currently deployed as [@dejossen](http://twitter.com/dejossen), [@dejossen@mastodon-belgium.be](https://mastodon-belgium.be/@dejossen) and [@dejossen.bsky.social](https://bsky.app/profile/dejossen.bsky.social).

Currently used to post lines from the absurdist play *De Jossen* by Tom Lanoye. That's where the name of this bot comes from. In March 2023, I rewrote this bot so it became more general and can be used for any .txt-based lines of content.

The full play got manually restructured to 426 lines of each 140 characters max, starting from the [original text](https://github.com/Forceflow/josbot/raw/main/De-Jossen.-Val-en-revival-der-saamhorigheid.pdf) which was released publicly on 2014 on Tom Lanoye's website. Tried to keep consistency when splitting lines in multiple posts, so there's never a split mid-sentence.

From the original PDF:

> De tekst van De Jossen. Val en revival der saamhorigheid mag vrij worden gedownload en verspreid.
> Opvoeringen, geheel of gedeeltelijk, mogen pas plaatsvinden na een voorafgaande schriftelijke afspraak
> met SABAM

I'm assuming running Josbot is not a *rendition* but a *distribution* of the source material, which is explicitly allowed.


