# josbot

## What

A Twitter bot that tweets random quotes from the play "De Jossen" by Tom Lanoye. Live on [@dejossen](http://twitter.com/dejossen).

## Tekst
Tekst werd aangepast voor 140 tekens, vertrekkende van de [originele tekst](http://www.lanoye.be/tom/wp-content/uploads/2012/10/De-Jossen.-Val-en-revival-der-saamhorigheid.pdf) die in 2014 werd vrijgegeven op de site van Tom Lanoye. Hierbij werd geprobeerd om de consistentie van het origineel zoveel mogelijk te bewaren.

## Rechten
Uit de originele pdf:

> De tekst van De Jossen. Val en revival der saamhorigheid mag vrij worden gedownload en verspreid.
> Opvoeringen, geheel of gedeeltelijk, mogen pas plaatsvinden na een voorafgaande schriftelijke afspraak
> met SABAM

Verondersteld wordt dat het in deze kwestie geen *opvoering* betreft maar een *verspreiding* van de tekst.

## Technical

Written for Python 3.0+ (but will run with on 2.6 with some print quirks). Required libraries: [Tweepy](http://www.tweepy.org/) and [YAML](http://www.yaml.org/). For example, in most recent Ubuntu versions, `sudo apt-get install python python-tweepy python-yaml` will install all requirements.

First run of the program will create a settings file (*settings.yml*) in which you have to fill in Twitter API details.
After that, run `python3 josbot.py` to start the bot.

