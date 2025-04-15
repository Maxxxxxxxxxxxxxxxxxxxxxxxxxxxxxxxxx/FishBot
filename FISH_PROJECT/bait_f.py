# # import telebot
# # from telebot import types
# # import json
# # import os
# # from secrets import secrets
# # from logic_json import *
# #
# #
# # token = secrets.get('BOT_API_TOKEN')
# # bot = telebot.TeleBot(token)
# #
# #
# #
# #
# #
# #
# # # Путь к папке и файлу
# # JSON_FOLDER = 'json'  # Название папки
# # SAVE_FILE_BAIT = os.path.join(JSON_FOLDER, 'selected_bait.json')  # Полный путь к файлу
# #
# #
# # # Загрузка состояния из файла
# # if os.path.exists(SAVE_FILE_BAIT):
# #     with open(SAVE_FILE_BAIT, 'r', encoding='utf-8') as z:
# #         selected_bait = json.load(z)
# # else:
# #     selected_bait = {}
# #
# # def load_bait_select():
# #     if os.path.exists(SAVE_FILE_BAIT):
# #         with open(SAVE_FILE_BAIT, 'r', encoding='utf-8') as file:
# #             return json.load(file)
# #     return {}
# #
# # # Функция для сохранения состояния в файл
# # def save_state_bait(selected_bait):
# #     with open(SAVE_FILE_BAIT, 'w', encoding='utf-8') as z:
# #         json.dump(selected_bait, z, ensure_ascii=False, indent=4)
# #
# # # def count_bait():
# # #     count_bait = 20
# # #     return (count_bait)
# #
# #
# # # Функция для создания клавиатуры с учетом выбранных кнопок
# # def create_markup_bait(user_selected_bait):
# #     print("user_selected_baitCREATE",user_selected_bait)
# #     markup = types.InlineKeyboardMarkup(row_width=1)
# #     buttons = [
# #         types.InlineKeyboardButton(f"{'✅ ' if 'Worms' in user_selected_bait else '80$ '}Worms 🐛 x20", callback_data="Worms"),
# #         types.InlineKeyboardButton(f"{'✅ ' if 'Leeches' in user_selected_bait else '500$ '}Leeches 🦐 x20", callback_data="Leeches"),
# #         types.InlineKeyboardButton(f"{'✅ ' if 'Magnet' in user_selected_bait else '500$ '}Magnet 🧲 x20", callback_data="Magnet"),
# #         #XP_Fish
# #         #Fish
# #         types.InlineKeyboardButton("back", callback_data='button_back')
# #     ]
# #     markup.add(*buttons)
# #     return markup
# #
# # # Функция test_f, которая отправляет сообщение с кнопками
# # #@bot.callback_query_handler(func=lambda call: call.data in ['bait1', 'bait2', 'bait3'])
# # @bot.callback_query_handler(func=lambda call: True)
# # def bait_func(chat_id):
# #     print("bait_func")
# #     user_id = str(chat_id)  # Используем строку, так как JSON ключи должны быть строками
# #
# #     # Проверяем, есть ли сохранённые данные для текущего пользователя
# #     selected_bait = load_bait_select()
# #     # print("68 selected_bait = load_bait_select()",selected_bait)
# #     if user_id not in selected_bait:
# #         selected_bait[user_id] = "Empty"
# #         # print("72 selected_bait ", selected_bait)
# #         bait_f.save_state_bait(selected_bait)
# #     user_selected_buttons = selected_bait[user_id]
# #
# #
# #
# #     # print(user_selected_buttons,'user_selected_buttons')
# #     # print(load_bait_select()[user_id],"Через лоад")
# #
# #     # Создаем клавиатуру с тремя кнопками
# #     markup = create_markup_bait(user_selected_buttons)
# #
# #     # Отправляем сообщение с кнопками
# #     bot.send_message(chat_id, "Choose fishing bait:", reply_markup=markup)
# #
# # # Обработчик callback-запросов
# # @bot.callback_query_handler(func=lambda call: call.data in ['Worms', 'Leeches', 'Magnet'])
# # def callback_query_bait(call):
# #     print("callback_query_bait")
# #     user_id = str(call.from_user.id)  # Используем строку, так как JSON ключи должны быть строками
# #     button_id = call.data
# #     user_money = load_money_data()
# #     selected_bait = load_bait_select()
# #     print("selected_bait[user_id]", selected_bait[user_id])
# #
# #     if user_id not in selected_bait:
# #         selected_bait[user_id] = "Empty"
# #
# #     user_bait_data = load_bait_data()
# #
# #
# #
# #     if button_id in selected_bait[user_id] and user_bait_data[user_id][button_id] != 0:
# #         print("107 убрать наживку")
# #
# #         # Если кнопка уже выбрана, убираем её из списка
# #         user_bait_data = load_bait_data()
# #         # user_bait_data[user_id][button_id] -= 20
# #         selected_bait[user_id] = "Empty"
# #         # print(selected_bait,"должно быть емпти")
# #         save_state_bait(selected_bait)
# #         save_bait_data(user_bait_data)
# #         print(user_bait_data[user_id],"user_bait_data В ФУНКЦИИ = 0")
# #         save_money_data(user_money)
# #     # else:
# #     #     # Если выбрано меньше одной кнопки, добавляем новую
# #     #     selected_bait[user_id] = (button_id)
# #     #     # print("111 baitf", selected_bait[user_id])
# #
# #     elif button_id in "Empty" and user_bait_data[user_id][button_id] != 0:
# #         print("121 baitf")
# #         selected_bait[user_id] = (button_id)
# #         save_state_bait(selected_bait)
# #
# #     elif selected_bait[user_id] in "Empty":
# #         print("104 baitf")
# #         selected_bait[user_id] = (button_id)
# #         save_state_bait(selected_bait)
# #         # else:
# #         #     bot.answer_callback_query(call.id, "You can select no more than two baits together", show_alert=True)
# #         #     return
# #     # Сохраняем состояние после каждого изменения
# #     save_state_bait(selected_bait)
# #     # print('selected_bait',selected_bait.get(user_id, []))
# #
# #     # Обновляем сообщение с кнопками
# #     updated_markup_bait = create_markup_bait(selected_bait.get(user_id, []))
# #     bot.edit_message_reply_markup(
# #         chat_id=call.message.chat.id,
# #         message_id=call.message.message_id,
# #         reply_markup=updated_markup_bait
# #     )
# #
# #
# #
# # def get_bait_number(bait_type):
# #     baits = ["Empty", "Magnet", "XP_Fish", "Worms", "Leeches", "Fish"]
# #     for i, bait in enumerate(baits, start=1):
# #         if bait == bait_type:
# #             return i
# #     return None
#
#
# import telebot
# from telebot import types
# import json
# import os
# from secrets import secrets
# from logic_json import *
#
# token = secrets.get('BOT_API_TOKEN')
# bot = telebot.TeleBot(token)
#
# # Путь к папке и файлу
# JSON_FOLDER = 'json'
# SAVE_FILE_BAIT = os.path.join(JSON_FOLDER, 'selected_bait.json')
#
#
# def load_bait_select():
#     if os.path.exists(SAVE_FILE_BAIT):
#         with open(SAVE_FILE_BAIT, 'r', encoding='utf-8') as file:
#             return json.load(file)
#     return {}
#
#
# def save_state_bait(selected_bait):
#     with open(SAVE_FILE_BAIT, 'w', encoding='utf-8') as z:
#         json.dump(selected_bait, z, ensure_ascii=False, indent=4)
#
#
# def create_markup_bait(user_selected_bait):
#     markup = types.InlineKeyboardMarkup(row_width=1)
#     buttons = [
#         types.InlineKeyboardButton(f"{'✅ ' if user_selected_bait == 'Worms' else '80$ '}Worms 🐛 x20",
#                                    callback_data="Worms"),
#         types.InlineKeyboardButton(f"{'✅ ' if user_selected_bait == 'Leeches' else '500$ '}Leeches 🦐 x20",
#                                    callback_data="Leeches"),
#         types.InlineKeyboardButton(f"{'✅ ' if user_selected_bait == 'Magnet' else '500$ '}Magnet 🧲 x20",
#                                    callback_data="Magnet"),
#         types.InlineKeyboardButton("back", callback_data='button_shop')#button_shop/button_back
#     ]
#     markup.add(*buttons)
#     return markup
#
#
# def bait_func(chat_id, message_id=None):
#     user_id = str(chat_id)
#     selected_bait = load_bait_select()
#
#     if user_id not in selected_bait:
#         selected_bait[user_id] = "Empty"
#         save_state_bait(selected_bait)
#
#     user_selected_buttons = selected_bait[user_id]
#     markup = create_markup_bait(user_selected_buttons)
#
#     if message_id:  # Если передан message_id, редактируем существующее сообщение
#         try:
#             bot.edit_message_text(
#                 chat_id=chat_id,
#                 message_id=message_id,
#                 text="Choose fishing bait:",
#                 reply_markup=markup
#             )
#         except Exception as e:
#             print(f"Error editing message: {e}")
#             bot.send_message(chat_id, "Choose fishing bait:", reply_markup=markup)
#     else:  # Если message_id не передан, отправляем новое сообщение
#         bot.send_message(chat_id, "Choose fishing bait:", reply_markup=markup)
#
#
# def callback_query_bait(call):
#     user_id = str(call.from_user.id)
#     button_id = call.data
#     selected_bait = load_bait_select()
#
#     if user_id not in selected_bait:
#         selected_bait[user_id] = "Empty"
#
#     user_bait_data = load_bait_data()
#
#     if button_id == selected_bait.get(user_id, "Empty") and user_bait_data[user_id].get(button_id, 0) > 0:
#         selected_bait[user_id] = "Empty"
#     else:
#         selected_bait[user_id] = button_id
#
#     save_state_bait(selected_bait)
#
#     updated_markup = create_markup_bait(selected_bait.get(user_id, "Empty"))
#
#     try:
#         bot.edit_message_reply_markup(
#             chat_id=call.message.chat.id,
#             message_id=call.message.message_id,
#             reply_markup=updated_markup
#         )
#     except Exception as e:
#         print(f"Error updating markup: {e}")
#
#     bot.answer_callback_query(call.id)
#
#
# def get_bait_number(bait_type):
#     baits = ["Empty", "Magnet", "XP_Fish", "Worms", "Leeches", "Fish"]
#     for i, bait in enumerate(baits, start=1):
#         if bait == bait_type:
#             return i
#     return None

import telebot
from telebot import types
import json
import os
from secrets import secrets
from logic_json import *

token = secrets.get('BOT_API_TOKEN')
bot = telebot.TeleBot(token)

# Путь к папке и файлу
JSON_FOLDER = 'json'
SAVE_FILE_BAIT = os.path.join(JSON_FOLDER, 'selected_bait.json')

def load_bait_select():
    if os.path.exists(SAVE_FILE_BAIT):
        with open(SAVE_FILE_BAIT, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

def save_state_bait(selected_bait):
    with open(SAVE_FILE_BAIT, 'w', encoding='utf-8') as z:
        json.dump(selected_bait, z, ensure_ascii=False, indent=4)

def create_markup_bait(user_selected_bait):
    markup = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton(f"{'✅ ' if user_selected_bait == 'Worms' else '80$ '}Worms 🐛 x20",
                                 callback_data="Worms"),
        types.InlineKeyboardButton(f"{'✅ ' if user_selected_bait == 'Leeches' else '500$ '}Leeches 🦐 x20",
                                 callback_data="Leeches"),
        types.InlineKeyboardButton(f"{'✅ ' if user_selected_bait == 'Magnet' else '500$ '}Magnet 🧲 x20",
                                 callback_data="Magnet"),
        types.InlineKeyboardButton("back", callback_data='button_shop')
    ]
    markup.add(*buttons)
    return markup

def bait_func(chat_id, inline_message_id=None, message_id=None):
    user_id = str(chat_id)
    selected_bait = load_bait_select()

    if user_id not in selected_bait:
        selected_bait[user_id] = "Empty"
        save_state_bait(selected_bait)

    current_bait = selected_bait.get(user_id, "Empty")
    markup = create_markup_bait(current_bait)

    if inline_message_id:  # Inline режим
        try:
            bot.edit_message_text(
                inline_message_id=inline_message_id,
                text="Choose fishing bait:",
                reply_markup=markup
            )
        except Exception as e:
            print(f"Error editing inline message: {e}")
    elif message_id:  # Обычный режим (редактирование)
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="Choose fishing bait:",
                reply_markup=markup
            )
        except Exception as e:
            print(f"Error editing message: {e}")
            bot.send_message(chat_id, "Choose fishing bait:", reply_markup=markup)
    else:  # Обычный режим (новое сообщение)
        bot.send_message(chat_id, "Choose fishing bait:", reply_markup=markup)

def callback_query_bait(call):
    user_id = str(call.from_user.id)
    button_id = call.data
    user_money = load_money_data()
    selected_bait = load_bait_select()
    user_bait_data = load_bait_data()

    if user_id not in selected_bait:
        selected_bait[user_id] = "Empty"

    price_map = {
        "Worms": 80,
        "Leeches": 500,
        "Magnet": 500
    }

    # Если наживка уже выбрана и есть в инвентаре
    if button_id == selected_bait.get(user_id, "Empty") and user_bait_data[user_id].get(button_id, 0) > 0:
        selected_bait[user_id] = "Empty"
    else:
        # Проверяем наличие денег или наживки в инвентаре
        if user_bait_data[user_id].get(button_id, 0) > 0:
            selected_bait[user_id] = button_id
        else:
            price = price_map.get(button_id, 0)
            if user_money.get(user_id, 0) >= price:
                user_money[user_id] -= price
                selected_bait[user_id] = button_id
                user_bait_data[user_id][button_id] = user_bait_data[user_id].get(button_id, 0) + 20
                save_money_data(user_money)
            else:
                bot.answer_callback_query(call.id, text="You don't have enough money(", show_alert=False)
                return

    save_state_bait(selected_bait)
    save_bait_data(user_bait_data)
    updated_markup = create_markup_bait(selected_bait.get(user_id, "Empty"))

    try:
        if hasattr(call, 'inline_message_id'):  # Inline режим
            bot.edit_message_text(
                inline_message_id=call.inline_message_id,
                text="Choose fishing bait:",
                reply_markup=updated_markup
            )
        else:  # Обычный режим
            bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=updated_markup
            )
    except Exception as e:
        print(f"Error updating markup: {e}")

    bot.answer_callback_query(call.id)

def get_bait_number(bait_type):
    baits = ["Empty", "Magnet", "XP_Fish", "Worms", "Leeches", "Fish"]
    for i, bait in enumerate(baits, start=1):
        if bait == bait_type:
            return i
    return None