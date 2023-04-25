import telegram
from telegram.ext import Updater, MessageHandler, Filters
from langdetect import detect
import requests
from bs4 import BeautifulSoup
import json
import requests


TOKEN = '6289732281:AAGjFFF6mPQBMQDYPt-kMXA-YZc8jcEY42k'

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
            "to": 10
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
    """Обработчик команды /start."""
    context.bot.send_message(chat_id=update.effective_chat.id,
                            text="Привет! Введите список продуктов через запятую, и я найду для вас рецепты блюд. Также можете указать через запятную особенности блюда: вегетарианское, без молока, без глютена")


def find_recipes(update, context):
    # Получаем введенные продукты и определяем язык
    lang = detect(update.message.text)
    query = update.message.text.lower()
    vegetarian = False
    gluten_free = False
    dairy_free = False

    # Проверяем, есть ли в запросе фильтры
    if "вегетарианский" in query:
        vegetarian = True
    if "без глютена" in query:
        gluten_free = True
    if "без молока" in query:
        dairy_free = True

    # Выбираем API-сервис на основе языка
    if lang == 'ru':
        api = EdimDomaAPI(url)
    else:
        app_id = "0444e0ee"
        app_key = "d27b186ea5810d2379393198a8096486"
        api = EdamamAPI(app_id, app_key)

    # Получаем список рецептов по запросу
    recipes = api.search_recipes(query, vegetarian, gluten_free, dairy_free)

    # Отправляем результат пользователю
    if not recipes:
        context.bot.send_message(chat_id=update.effective_chat.id, text='К сожалению, я не смог найти рецептов с такими продуктами и фильтрами.')
    else:
        # Отправляем найденные рецепты пользователю
        for recipe in recipes:
            if lang == 'ru':
                title = recipe.find('a', class_='b-recipe-preview__link').text
                url = 'https://www.edimdoma.ru' + recipe.find('a', class_='b-recipe-preview__link')['href']
                ingredients = recipe.find_all('li', class_='b-recipe-preview__ingredient')
                ingredients = [ingredient.text.strip() for ingredient in ingredients]
                ingredients = '\n'.join(ingredients)
                context.bot.send_message(chat_id=update.effective_chat.id, text=f'<b>{title}</b>\n{ingredients}\n<a href="{url}">Ссылка на рецепт</a>', parse_mode=telegram.ParseMode.HTML)
            else:
                title = recipe["label"]
                url = recipe["url"]
                ingredients = recipe["ingredientLines"]
                ingredients = '\n'.join(ingredients)
                context.bot.send_message(chat_id=update.effective_chat.id, text=f'<b>{title}</b>\n{ingredients}\n<a href="{url}">Ссылка на рецепт</a>', parse_mode=telegram.ParseMode.HTML)


def main():
    # Инициализация бота
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Регистрация обработчиков
    start_handler = MessageHandler(Filters.regex('^/start$'), start)
    recipe_handler = MessageHandler(Filters.text, find_recipes)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(recipe_handler)

    # Запуск бота
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()