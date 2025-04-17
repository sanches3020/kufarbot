import requests
from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bs4 import BeautifulSoup
from loader import cursor, Bot
import json
from aiogram import types

def parse_website(url, class_name, inner_class_name):
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Ошибка запроса:{response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    parsed_data = []

    elements = soup.find_all(class_=class_name)
    for element in elements:
        text = element.get_text(strip=True)

        img_tag = element.find('img')
        img_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else None

        inner_element = element.find(class_=inner_class_name)
        inner_text = inner_element.get_text(strip=True) if inner_element else None

        link_url = element.get('href') if element.has_attr('href') else None
        link_url = link_url.split('?')[0] if link_url else None

        parsed_data.append([text, img_url, inner_text, link_url])

    return parsed_data

async def parser_update(id, bot: Bot):
    
    cursor.execute("SELECT url FROM MyTable WHERE id = ?", (id,))
    user_data = cursor.fetchone()

    if not user_data:
        print(f"Не удалось найти пользователя с ID: {id}")
        return

    url = user_data[0]

    class_names = "styles_wrapper__5FoK7"
    inner_class_name = "styles_secondary__MzdEb"

    result = parse_website(url, class_names, inner_class_name)[:5]

    try:
        with open(f"{id}.json", "r", encoding="utf-8") as file:
            old_result = json.load(file)
    except FileNotFoundError:
        old_result = []

    data = [item for item in result if item not in old_result]

    with open(f"{id}.json", "w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=4)

        for mess in data:
            builder = InlineKeyboardBuilder()
            builder.add(types.InlineKeyboardButton(text='Открыть объявление',
                web_app=WebAppInfo(url=mess[3])))

            await bot.send_photo(caption=f'{mess[0]}\{mess[2]}',
                chat_id=id, photo=mess[1],
                reply_markup=builder.as_markup(resize_keyboard=True))