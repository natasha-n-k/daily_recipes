import telegram
from telegram.ext import Updater, MessageHandler, Filters
from langdetect import detect
import requests
import json

TOKEN = ''

class EdamamAPI:
    def __init__(self, app_id, app_key):
        self.url = "https://api.edamam.com/search"
        self.app_id = app_id
        self.app_key = app_key

    def search_recipes(self, query, vegetarian=False, gluten_free=False, dairy_free=False):
        params = {
            "q": query,
            "app_id": self.app_id,
            "app_key": self.app_key,
            "from": 0,
            "to": 5
        }

        if vegetarian:
            params["health"] = "vegetarian"

        if gluten_free:
            params["health"] = "gluten-free"

        if dairy_free:
            params["health"] = "dairy-free"

        response = requests.get(self.url, params=params)
        data = json.loads(response.text)

        if "hits" not in data:
            return []

        recipes = []
        for hit in data["hits"]:
            recipe = hit["recipe"]
            recipes.append(recipe)

        return recipes
    

def start(update, context):
    """Handler function for the /start command."""
    context.bot.send_message(chat_id=update.effective_chat.id,
                            text="Hi! Send a message to the bot with a list of ingredients separated by commas. You can also add one or more of the following filters: 'vegetarian', 'gluten-free', and 'dairy-free'.")


def find_recipes(update, context):
    # Get input ingredients and detect language
    lang = detect(update.message.text)
    query = update.message.text.lower()
    vegetarian = False
    gluten_free = False
    dairy_free = False

    # Check if filters are included in the query
    if "вегетарианский" in query:
        vegetarian = True
    if "без глютена" in query:
        gluten_free = True
    if "без молока" in query:
        dairy_free = True

    app_id = ""
    app_key = ""
    api = EdamamAPI(app_id, app_key)

    # Get recipe list based on the query
    recipes = api.search_recipes(query, vegetarian, gluten_free, dairy_free)

    # Send results back to user
    if not recipes:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Sorry, I could not find any recipes with these ingredients and dietary restrictions.')
    else:
        # Send found recipes to user
        for recipe in recipes:
            title = recipe["label"]
            url = recipe["url"]
            ingredients = recipe["ingredientLines"]
            ingredients = '\n'.join(ingredients)
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'<b>{title}</b>\n{ingredients}\n<a href="{url}">Ссылка на рецепт</a>', parse_mode=telegram.ParseMode.HTML)


def main():
    #  Initialize the bot
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register the handlers
    start_handler = MessageHandler(Filters.regex('^/start$'), start)
    recipe_handler = MessageHandler(Filters.text, find_recipes)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(recipe_handler)

    # Bot launch
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
