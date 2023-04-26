## The daily recipes

### Description

This is a Telegram bot that searches for recipes based on user input. It uses the Edamam Recipe Search API to search for recipes and can filter by vegetarian, gluten-free, and dairy-free options.

##


### Technology stack

This bot uses the Edamam Recipe Search API to find recipes based on ingredients and filters.

- Python 3
- python-telegram-bot
- langdetect
- requests

##

### Installation

- Clone or download the repository.
- Install the required libraries by running 
```pip install python-telegram-bot``` 
- Obtain a Telegram Bot API token by following the instructions [here](https://core.telegram.org/bots#creating-a-new-bot).
- Run the script by running 
``` python bot.py``` 

##

### Usage

- Start a conversation with your bot on Telegram. ``` /start``` 
- Send a message to the bot with a list of ingredients separated by commas. You can also add one or more of the following filters: "vegetarian", "gluten-free", and "dairy-free".
- The bot will reply with up to 10 recipes that match the ingredients and filters you specified.

##
### Plans

In the future, I plan to be able to search both in English on an English-language site and on a Russian-language site in Russian. Until I found a Russian site with an open API

