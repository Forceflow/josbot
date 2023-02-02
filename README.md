# josbot v0.5
A Twitter bot that tweets random quotes from the play *De Jossen* by Tom Lanoye. Live on [@dejossen](http://twitter.com/dejossen).

One could easily use this bot to tweet other content, by replacing the lines provided in `quotes.txt`. The code is very general and documented.

## Text
The full play got reduced to 426 lines of each 140 characters max, starting from the [original text](http://www.lanoye.be/tom/wp-content/uploads/2012/10/De-Jossen.-Val-en-revival-der-saamhorigheid.pdf) which was released publicly on 2014 on Tom Lanoye's website. Tried to keep consistency when splitting lines in multiple tweets, so there's never a split mid-sentence.

## Requirements

Written for Python 3. Required libraries: [Tweepy](http://www.tweepy.org/) for Twitter API interaction and [YAML](http://www.yaml.org/) for reading/writing the settings file.  
 * In most recent Ubuntu versions: `sudo apt-get install python3 python3-tweepy python3-yaml python3-mastodon`
 * Using pip: `pip3 install tweepy pyaml Mastodon.py`

First run of the program will create a settings file (*settings.yml*) in which you have to fill in Twitter API details.
After that, run `python3 josbot.py` to start the bot.

## Rights
From the original PDF:

> De tekst van De Jossen. Val en revival der saamhorigheid mag vrij worden gedownload en verspreid.
> Opvoeringen, geheel of gedeeltelijk, mogen pas plaatsvinden na een voorafgaande schriftelijke afspraak
> met SABAM

I'm assuming running Josbot is not a *rendition* but a *distribution* of the source material, which is explicitly allowed.
