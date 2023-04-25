import telegram
from telegram.ext import Updater, MessageHandler, Filters
from langdetect import detect
import requests
from bs4 import BeautifulSoup


TOKEN = '6289732281:AAGjFFF6mPQBMQDYPt-kMXA-YZc8jcEY42k'

class EdamamAPI:
    def __init__(self, token):
        self.token = token

    def 


def start(update, context):
    """Обработчик команды /start."""
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Введите список продуктов через запятую, и я найду для вас рецепты блюд.")


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
        api = EdamamAPI(url)

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
                title = recipe.find('h3', class_='fixed-recipe-card__h3').text.strip()
                url = recipe.find('a', class_='fixed-recipe-card__title-link')['href']
                ingredients = recipe.find('div', class_='fixed-recipe-card__ingredients').text.strip()
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