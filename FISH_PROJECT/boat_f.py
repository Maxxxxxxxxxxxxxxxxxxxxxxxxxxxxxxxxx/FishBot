# # import telebot
# # from telebot import types
# # import json
# # import os
# # from secrets import secrets
# # from logic_json import *
# #
# # token = secrets.get('BOT_API_TOKEN')
# # bot = telebot.TeleBot(token)
# #
# #
# #
# # # Путь к папке и файлу
# # JSON_FOLDER = 'json'  # Название папки
# # SAVE_FILE_BOAT = os.path.join(JSON_FOLDER, 'user_boat.json')  # Полный путь к файлу
# #
# #
# # # Загрузка состояния из файла
# # if os.path.exists(SAVE_FILE_BOAT):
# #     with open(SAVE_FILE_BOAT, 'r', encoding='utf-8') as v:
# #         selected_boat = json.load(v)
# # else:
# #     selected_boat = {}
# #
# # def load_boat_select():
# #     if os.path.exists(SAVE_FILE_BOAT):
# #         with open(SAVE_FILE_BOAT, 'r', encoding='utf-8') as file:
# #             return json.load(file)
# #     return {}
# # # Функция для сохранения состояния в файл
# # def save_state_boat(selected_boat):
# #     with open(SAVE_FILE_BOAT, 'w', encoding='utf-8') as v:
# #         json.dump(selected_boat, v, ensure_ascii=False, indent=4)
# #
# #
# #
# # # Функция для создания клавиатуры с учетом выбранных кнопок
# # def create_markup_boat(user_selected_boat):
# #     markup = types.InlineKeyboardMarkup(row_width=1)
# #     buttons = [
# #         types.InlineKeyboardButton(f"{'✅ ' if 'boat1' in user_selected_boat else '5000$ '}Rowboat 🚣", callback_data="boat1"), #🚣🚤🛥️⛵⛴️🚢
# #         types.InlineKeyboardButton(f"{'✅ ' if 'boat2' in user_selected_boat else '25000$ '}Fishing Boat 🚤", callback_data="boat2"),
# #         types.InlineKeyboardButton(f"{'✅ ' if 'boat3' in user_selected_boat else '100000$ '}Speedboat 🛥️", callback_data="boat3"),
# #         types.InlineKeyboardButton(f"{'✅ ' if 'boat4' in user_selected_boat else '250000$ '}Sailboat ⛵", callback_data="boat4"),
# #         types.InlineKeyboardButton(f"{'✅ ' if 'boat5' in user_selected_boat else '1000000$ '}Ferryboat ⛴️", callback_data="boat5"),
# #         types.InlineKeyboardButton(f"{'✅ ' if 'boat6' in user_selected_boat else '20000000$ '}Yacht 🚢", callback_data="boat6"),
# #         # types.InlineKeyboardButton(f"{'✅ ' if 'boat7' in user_selected_boat else '1000000$ '}Lava rod 🎣🔥", callback_data="rod7"),
# #         # types.InlineKeyboardButton(f"{'✅ ' if 'boat8' in user_selected_boat else '10000000$ '}Magma rod 🎣🔥", callback_data="rod8"),
# #         types.InlineKeyboardButton("back", callback_data='button_back')
# #     ]
# #
# #     markup.add(*buttons)
# #     return markup
# #
# # # Функция test_f, которая отправляет сообщение с кнопками
# # # @bot.callback_query_handler(func=lambda call: call.data in ["rod1", 'rod2', 'rod3'])
# # @bot.callback_query_handler(func=lambda call: True)
# # def boat_func(chat_id):
# #     user_id = str(chat_id)  # Используем строку, так как JSON ключи должны быть строками
# #
# #     # Проверяем, есть ли сохранённые данные для текущего пользователя
# #     user_selected_buttons = selected_boat.get(user_id, [])
# #
# #
# #
# #     # Создаем клавиатуру с тремя кнопками
# #     markup = create_markup_boat(user_selected_buttons)
# #
# #     # Отправляем сообщение с кнопками
# #     bot.send_message(chat_id, "Choose boat:", reply_markup=markup)
# #
# #
# # # Обработчик callback-запросов
# # @bot.callback_query_handler(func=lambda call: call.data in ["boat1", 'boat2', 'boat3',"boat4", 'boat5', 'boat6'])
# # def callback_query_boat(call):
# #     user_id = str(call.from_user.id)  # Используем строку, так как JSON ключи должны быть строками
# #     button_id = call.data
# #     user_money = load_money_data()
# #
# #
# #     if user_id not in selected_boat:
# #         selected_boat[user_id] = "Empty"
# #
# #
# #
# #     if button_id in selected_boat[user_id]:
# #         # Если кнопка уже выбрана, убираем её из списка
# #         selected_boat[user_id] = "Empty"
# #     else:
# #
# #         match button_id:
# #             case "boat1":
# #
# #                 if user_money[user_id] >= 5000:
# #                     user_money[user_id] -= 5000
# #                     selected_boat[user_id] = (button_id)
# #                     save_money_data(user_money)
# #                 else:
# #                     bot.answer_callback_query(call.id, text="You don't have enough money(", show_alert=False)
# #                     return
# #             case "boat2":
# #                 if user_money[user_id] >= 25000:
# #                     user_money[user_id] -= 25000
# #                     selected_boat[user_id] = (button_id)
# #                     save_money_data(user_money)
# #                 else:
# #                     bot.answer_callback_query(call.id, text="You don't have enough money(", show_alert=False)
# #                     return
# #             case "boat3":
# #                 if user_money[user_id] >= 100000:
# #                     user_money[user_id] -= 100000
# #                     selected_boat[user_id] = (button_id)
# #                     save_money_data(user_money)
# #                 else:
# #                     bot.answer_callback_query(call.id, text="You don't have enough money(", show_alert=False)
# #                     return
# #             case "boat4":
# #                 if user_money[user_id] >= 250000:
# #                     user_money[user_id] -= 250000
# #                     selected_boat[user_id] = (button_id)
# #                     save_money_data(user_money)
# #                 else:
# #                     bot.answer_callback_query(call.id, text="You don't have enough money(", show_alert=False)
# #                     return
# #             case "boat5":
# #                 if user_money[user_id] >= 1000000:
# #                     user_money[user_id] -= 1000000
# #                     selected_boat[user_id] = (button_id)
# #                     save_money_data(user_money)
# #                 else:
# #                     bot.answer_callback_query(call.id, text="You don't have enough money(", show_alert=False)
# #                     return
# #             case "boat6":
# #                 if user_money[user_id] >= 20000000:
# #                     user_money[user_id] -= 20000000
# #                     selected_boat[user_id] = (button_id)
# #                     save_money_data(user_money)
# #                 else:
# #                     bot.answer_callback_query(call.id, text="You don't have enough money(", show_alert=False)
# #                     return
# #
# #
# #     # Сохраняем состояние после каждого изменения
# #     save_state_boat(selected_boat)
# #     save_money_data(user_money)
# #     # Обновляем сообщение с кнопками
# #     updated_markup_boat = create_markup_boat(selected_boat.get(user_id, []))
# #     bot.edit_message_reply_markup(
# #         chat_id=call.message.chat.id,
# #         message_id=call.message.message_id,
# #         reply_markup=updated_markup_boat
# #     )
# # def get_boat_number(boat_type):
# #     if boat_type in ["Empty",[]]:
# #         return 1
# #     return int(boat_type[-1])
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
# SAVE_FILE_BOAT = os.path.join(JSON_FOLDER, 'user_boat.json')
#
# # Загрузка состояния из файла
# if os.path.exists(SAVE_FILE_BOAT):
#     with open(SAVE_FILE_BOAT, 'r', encoding='utf-8') as v:
#         selected_boat = json.load(v)
# else:
#     selected_boat = {}
#
#
# def load_boat_select():
#     if os.path.exists(SAVE_FILE_BOAT):
#         with open(SAVE_FILE_BOAT, 'r', encoding='utf-8') as file:
#             return json.load(file)
#     return {}
#
#
# def save_state_boat(selected_boat):
#     with open(SAVE_FILE_BOAT, 'w', encoding='utf-8') as v:
#         json.dump(selected_boat, v, ensure_ascii=False, indent=4)
#
#
# def create_markup_boat(user_selected_boat):
#     markup = types.InlineKeyboardMarkup(row_width=1)
#     buttons = [
#         types.InlineKeyboardButton(f"{'✅ ' if user_selected_boat == 'boat1' else '5000$ '}Rowboat 🚣",
#                                    callback_data="boat1"),
#         types.InlineKeyboardButton(f"{'✅ ' if user_selected_boat == 'boat2' else '25000$ '}Fishing Boat 🚤",
#                                    callback_data="boat2"),
#         types.InlineKeyboardButton(f"{'✅ ' if user_selected_boat == 'boat3' else '100000$ '}Speedboat 🛥️",
#                                    callback_data="boat3"),
#         types.InlineKeyboardButton(f"{'✅ ' if user_selected_boat == 'boat4' else '250000$ '}Sailboat ⛵",
#                                    callback_data="boat4"),
#         types.InlineKeyboardButton(f"{'✅ ' if user_selected_boat == 'boat5' else '1000000$ '}Ferryboat ⛴️",
#                                    callback_data="boat5"),
#         types.InlineKeyboardButton(f"{'✅ ' if user_selected_boat == 'boat6' else '20000000$ '}Yacht 🚢",
#                                    callback_data="boat6"),
#         types.InlineKeyboardButton("back", callback_data='button_shop')
#     ]
#     markup.add(*buttons)
#     return markup
#
#
# def boat_func(chat_id, message_id=None):
#     user_id = str(chat_id)
#     selected_boat = load_boat_select()
#
#     if user_id not in selected_boat:
#         selected_boat[user_id] = "Empty"
#         save_state_boat(selected_boat)
#
#     current_boat = selected_boat.get(user_id, "Empty")
#     markup = create_markup_boat(current_boat)
#
#     if message_id:  # Если передан message_id, редактируем существующее сообщение
#         try:
#             bot.edit_message_text(
#                 chat_id=chat_id,
#                 message_id=message_id,
#                 text="Choose boat:",
#                 reply_markup=markup
#             )
#         except Exception as e:
#             print(f"Error editing message: {e}")
#             bot.send_message(chat_id, "Choose boat:", reply_markup=markup)
#     else:  # Если message_id не передан, отправляем новое сообщение
#         bot.send_message(chat_id, "Choose boat:", reply_markup=markup)
#
#
# def callback_query_boat(call):
#     user_id = str(call.from_user.id)
#     button_id = call.data
#     user_money = load_money_data()
#     selected_boat = load_boat_select()
#
#     if user_id not in selected_boat:
#         selected_boat[user_id] = "Empty"
#
#     price_map = {
#         "boat1": 5000,
#         "boat2": 25000,
#         "boat3": 100000,
#         "boat4": 250000,
#         "boat5": 1000000,
#         "boat6": 20000000
#     }
#
#     if button_id == selected_boat.get(user_id, "Empty"):
#         # Если лодка уже выбрана, снимаем выбор
#         selected_boat[user_id] = "Empty"
#     else:
#         # Проверяем, хватает ли денег
#         price = price_map.get(button_id, 0)
#         if user_money.get(user_id, 0) >= price:
#             user_money[user_id] -= price
#             selected_boat[user_id] = button_id
#             save_money_data(user_money)
#         else:
#             bot.answer_callback_query(call.id, text="You don't have enough money(", show_alert=False)
#             return
#
#     save_state_boat(selected_boat)
#
#     updated_markup = create_markup_boat(selected_boat.get(user_id, "Empty"))
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
# def get_boat_number(boat_type):
#     if not boat_type or boat_type == "Empty":
#         return 1
#     return int(boat_type[-1]) if boat_type[-1].isdigit() else 1

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
SAVE_FILE_BOAT = os.path.join(JSON_FOLDER, 'user_boat.json')

# Загрузка состояния из файла
if os.path.exists(SAVE_FILE_BOAT):
    with open(SAVE_FILE_BOAT, 'r', encoding='utf-8') as v:
        selected_boat = json.load(v)
else:
    selected_boat = {}


def load_boat_select():
    if os.path.exists(SAVE_FILE_BOAT):
        with open(SAVE_FILE_BOAT, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}


def save_state_boat(selected_boat):
    with open(SAVE_FILE_BOAT, 'w', encoding='utf-8') as v:
        json.dump(selected_boat, v, ensure_ascii=False, indent=4)


def create_markup_boat(user_selected_boat):
    markup = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton(f"{'✅ ' if user_selected_boat == 'boat1' else '5000$ '}Rowboat 🚣",
                                 callback_data="boat1"),
        types.InlineKeyboardButton(f"{'✅ ' if user_selected_boat == 'boat2' else '25000$ '}Fishing Boat 🚤",
                                 callback_data="boat2"),
        types.InlineKeyboardButton(f"{'✅ ' if user_selected_boat == 'boat3' else '100000$ '}Speedboat 🛥️",
                                 callback_data="boat3"),
        types.InlineKeyboardButton(f"{'✅ ' if user_selected_boat == 'boat4' else '250000$ '}Sailboat ⛵",
                                 callback_data="boat4"),
        types.InlineKeyboardButton(f"{'✅ ' if user_selected_boat == 'boat5' else '1000000$ '}Ferryboat ⛴️",
                                 callback_data="boat5"),
        types.InlineKeyboardButton(f"{'✅ ' if user_selected_boat == 'boat6' else '20000000$ '}Yacht 🚢",
                                 callback_data="boat6"),
        types.InlineKeyboardButton("back", callback_data='button_shop')
    ]
    markup.add(*buttons)
    return markup


def boat_func(chat_id, inline_message_id=None, message_id=None):
    user_id = str(chat_id)
    selected_boat = load_boat_select()

    if user_id not in selected_boat:
        selected_boat[user_id] = "Empty"
        save_state_boat(selected_boat)

    current_boat = selected_boat.get(user_id, "Empty")
    markup = create_markup_boat(current_boat)

    if inline_message_id:  # Режим inline
        try:
            bot.edit_message_text(
                inline_message_id=inline_message_id,
                text="Choose boat:",
                reply_markup=markup
            )
        except Exception as e:
            print(f"Error editing inline message: {e}")
    elif message_id:  # Обычный режим (редактирование)
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="Choose boat:",
                reply_markup=markup
            )
        except Exception as e:
            print(f"Error editing message: {e}")
            bot.send_message(chat_id, "Choose boat:", reply_markup=markup)
    else:  # Обычный режим (новое сообщение)
        bot.send_message(chat_id, "Choose boat:", reply_markup=markup)


def callback_query_boat(call):
    user_id = str(call.from_user.id)
    button_id = call.data
    user_money = load_money_data()
    selected_boat = load_boat_select()

    if user_id not in selected_boat:
        selected_boat[user_id] = "Empty"

    price_map = {
        "boat1": 5000,
        "boat2": 25000,
        "boat3": 100000,
        "boat4": 250000,
        "boat5": 1000000,
        "boat6": 20000000
    }

    if button_id == selected_boat.get(user_id, "Empty"):
        selected_boat[user_id] = "Empty"
    else:
        price = price_map.get(button_id, 0)
        if user_money.get(user_id, 0) >= price:
            user_money[user_id] -= price
            selected_boat[user_id] = button_id
            save_money_data(user_money)
        else:
            bot.answer_callback_query(call.id, text="You don't have enough money(", show_alert=False)
            return

    save_state_boat(selected_boat)
    updated_markup = create_markup_boat(selected_boat.get(user_id, "Empty"))

    try:
        if hasattr(call, 'inline_message_id'):  # Режим inline
            bot.edit_message_text(
                inline_message_id=call.inline_message_id,
                text="Choose boat:",
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


def get_boat_number(boat_type):
    if not boat_type or boat_type == "Empty":
        return 1
    return int(boat_type[-1]) if boat_type[-1].isdigit() else 1