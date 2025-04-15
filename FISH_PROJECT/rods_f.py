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
# # # Путь к папке и файлу
# # JSON_FOLDER = 'json'  # Название папки
# # SAVE_FILE_RODS = os.path.join(JSON_FOLDER, 'selected_rods.json')  # Полный путь к файлу
# #
# #
# #
# # # Загрузка состояния из файла
# # if os.path.exists(SAVE_FILE_RODS):
# #     with open(SAVE_FILE_RODS, 'r', encoding='utf-8') as f:
# #         selected_rods = json.load(f)
# # else:
# #     selected_rods = {}
# #
# # def load_rods_select():
# #     if os.path.exists(SAVE_FILE_RODS):
# #         with open(SAVE_FILE_RODS, 'r', encoding='utf-8') as file:
# #             return json.load(file)
# #     return {}
# # # Функция для сохранения состояния в файл
# # def save_state_rods(selected_rods):
# #     with open(SAVE_FILE_RODS, 'w', encoding='utf-8') as f:
# #         json.dump(selected_rods, f, ensure_ascii=False, indent=4)
# #
# #
# #
# # # Функция для создания клавиатуры с учетом выбранных кнопок
# # def create_markup_rods(user_selected_rods):
# #     markup = types.InlineKeyboardMarkup(row_width=1)
# #     buttons = [
# #         types.InlineKeyboardButton(f"{'✅ ' if 'rod1' in user_selected_rods else '100$ '}Plastic rod 🎣", callback_data="rod1"),
# #         types.InlineKeyboardButton(f"{'✅ ' if 'rod2' in user_selected_rods else '500$ '}Improved rod 🎣", callback_data="rod2"),
# #         types.InlineKeyboardButton(f"{'✅ ' if 'rod3' in user_selected_rods else '8000$ '}Steel rod 🎣", callback_data="rod3"),
# #         types.InlineKeyboardButton(f"{'✅ ' if 'rod4' in user_selected_rods else '50000$ '}Fiberglass rod 🎣", callback_data="rod4"),
# #         types.InlineKeyboardButton(f"{'✅ ' if 'rod5' in user_selected_rods else '100000$ '}Heavy rod 🎣", callback_data="rod5"),
# #         types.InlineKeyboardButton(f"{'✅ ' if 'rod6' in user_selected_rods else '250000$ '}Alloy rod 🎣🔥", callback_data="rod6"),
# #         types.InlineKeyboardButton(f"{'✅ ' if 'rod7' in user_selected_rods else '1000000$ '}Lava rod 🎣🔥", callback_data="rod7"),
# #         types.InlineKeyboardButton(f"{'✅ ' if 'rod8' in user_selected_rods else '10000000$ '}Magma rod 🎣🔥", callback_data="rod8"),
# #         types.InlineKeyboardButton("back", callback_data='button_shop')
# #     ]
# #     markup.add(*buttons)
# #     return markup
# #
# # # Функция test_f, которая отправляет сообщение с кнопками
# # # @bot.callback_query_handler(func=lambda call: call.data in ["rod1", 'rod2', 'rod3'])
# # @bot.callback_query_handler(func=lambda call: True)
# # def rods_func(chat_id):
# #     user_id = str(chat_id)  # Используем строку, так как JSON ключи должны быть строками
# #
# #     # Проверяем, есть ли сохранённые данные для текущего пользователя
# #     user_selected_buttons = selected_rods.get(user_id, [])
# #
# #
# #     # Создаем клавиатуру с тремя кнопками
# #     markup = create_markup_rods(user_selected_buttons)
# #
# #     # Отправляем сообщение с кнопками
# #     bot.send_message(chat_id, "Choose fishing rod:", reply_markup=markup)
# #
# # # Обработчик callback-запросов
# # @bot.callback_query_handler(func=lambda call: call.data in ["rod1", 'rod2', 'rod3',"rod4", 'rod5', 'rod6',"rod7", 'rod8'])
# # def callback_query_rods(call):
# #     user_id = str(call.from_user.id)  # Используем строку, так как JSON ключи должны быть строками
# #     button_id = call.data
# #     user_money = load_money_data()
# #
# #
# #     if user_id not in selected_rods:
# #         selected_rods[user_id] = "Empty"
# #
# #     if button_id in selected_rods[user_id]:
# #         # Если кнопка уже выбрана, убираем её из списка
# #         selected_rods[user_id] = "Empty"
# #     else:
# #         # Если выбрано меньше двух кнопок, добавляем новую
# #
# #         match button_id:
# #             case "rod1":
# #                 if user_money[user_id] >= 100:
# #                     user_money[user_id] -= 100
# #                     selected_rods[user_id]=(button_id)
# #                 else:
# #                     bot.answer_callback_query(call.id, text="You don't have enough money(", show_alert=False)
# #                     return
# #             case "rod2":
# #                 if user_money[user_id] >= 500:
# #                     user_money[user_id] -= 500
# #                     selected_rods[user_id]=(button_id)
# #                 else:
# #                     bot.answer_callback_query(call.id, text="You don't have enough money(", show_alert=False)
# #                     return
# #             case "rod3":
# #                 if user_money[user_id] >= 8000:
# #                     user_money[user_id] -= 8000
# #                     selected_rods[user_id]=(button_id)
# #                 else:
# #                     bot.answer_callback_query(call.id, text="You don't have enough money(", show_alert=False)
# #                     return
# #             case "rod4":
# #                 if user_money[user_id] >= 50000:
# #                     user_money[user_id] -= 50000
# #                     selected_rods[user_id]=(button_id)
# #                 else:
# #                     bot.answer_callback_query(call.id, text="You don't have enough money(", show_alert=False)
# #                     return
# #             case "rod5":
# #                 if user_money[user_id] >= 100000:
# #                     user_money[user_id] -= 100000
# #                     selected_rods[user_id]=(button_id)
# #                 else:
# #                     bot.answer_callback_query(call.id, text="You don't have enough money(", show_alert=False)
# #                     return
# #             case "rod6":
# #                 if user_money[user_id] >= 250000:
# #                     user_money[user_id] -= 250000
# #                     selected_rods[user_id]=(button_id)
# #                 else:
# #                     bot.answer_callback_query(call.id, text="You don't have enough money(", show_alert=False)
# #                     return
# #             case "rod7":
# #                 if user_money[user_id] >= 1000000:
# #                     user_money[user_id] -= 1000000
# #                     selected_rods[user_id]=(button_id)
# #                 else:
# #                     bot.answer_callback_query(call.id, text="You don't have enough money(", show_alert=False)
# #                     return
# #             case "rod8":
# #                 if user_money[user_id] >= 10000000:
# #                     user_money[user_id] -= 1000000
# #                     selected_rods[user_id]=(button_id)
# #                 else:
# #                     bot.answer_callback_query(call.id, text="You don't have enough money(", show_alert=False)
# #                     return
# #
# #
# #
# #
# #
# #     # Сохраняем состояние после каждого изменения
# #     save_state_rods(selected_rods)
# #     save_money_data(user_money)
# #     # Обновляем сообщение с кнопками
# #     updated_markup_rods = create_markup_rods(selected_rods.get(user_id, []))
# #     bot.edit_message_reply_markup(
# #         chat_id=call.message.chat.id,
# #         message_id=call.message.message_id,
# #         reply_markup=updated_markup_rods
# #     )
# # def get_rods_number(rods_type):
# #     if rods_type in ["Empty",[]]:
# #         return 1
# #     return int(rods_type[-1])
# # ------------------------------------------------------------------------------------------------------------------------------
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
# SAVE_FILE_RODS = os.path.join(JSON_FOLDER, 'selected_rods.json')
#
# # Загрузка состояния из файла
# if os.path.exists(SAVE_FILE_RODS):
#     with open(SAVE_FILE_RODS, 'r', encoding='utf-8') as f:
#         selected_rods = json.load(f)
# else:
#     selected_rods = {}
#
#
# def load_rods_select():
#     if os.path.exists(SAVE_FILE_RODS):
#         with open(SAVE_FILE_RODS, 'r', encoding='utf-8') as file:
#             return json.load(file)
#     return {}
#
#
# def save_state_rods(selected_rods):
#     with open(SAVE_FILE_RODS, 'w', encoding='utf-8') as f:
#         json.dump(selected_rods, f, ensure_ascii=False, indent=4)
#
#
# def create_markup_rods(user_selected_rod):
#     markup = types.InlineKeyboardMarkup(row_width=1)
#     buttons = [
#         types.InlineKeyboardButton(f"{'✅ ' if user_selected_rod == 'rod1' else '100$ '}Plastic rod 🎣",
#                                    callback_data="rod1"),
#         types.InlineKeyboardButton(f"{'✅ ' if user_selected_rod == 'rod2' else '500$ '}Improved rod 🎣",
#                                    callback_data="rod2"),
#         types.InlineKeyboardButton(f"{'✅ ' if user_selected_rod == 'rod3' else '8000$ '}Steel rod 🎣",
#                                    callback_data="rod3"),
#         types.InlineKeyboardButton(f"{'✅ ' if user_selected_rod == 'rod4' else '50000$ '}Fiberglass rod 🎣",
#                                    callback_data="rod4"),
#         types.InlineKeyboardButton(f"{'✅ ' if user_selected_rod == 'rod5' else '100000$ '}Heavy rod 🎣",
#                                    callback_data="rod5"),
#         types.InlineKeyboardButton(f"{'✅ ' if user_selected_rod == 'rod6' else '250000$ '}Alloy rod 🎣🔥",
#                                    callback_data="rod6"),
#         types.InlineKeyboardButton(f"{'✅ ' if user_selected_rod == 'rod7' else '1000000$ '}Lava rod 🎣🔥",
#                                    callback_data="rod7"),
#         types.InlineKeyboardButton(f"{'✅ ' if user_selected_rod == 'rod8' else '10000000$ '}Magma rod 🎣🔥",
#                                    callback_data="rod8"),
#         types.InlineKeyboardButton("back", callback_data='button_shop')
#     ]
#     markup.add(*buttons)
#     return markup
#
#
# def rods_func(chat_id, message_id=None):
#     user_id = str(chat_id)
#     selected_rods = load_rods_select()
#
#     if user_id not in selected_rods:
#         selected_rods[user_id] = "Empty"
#         save_state_rods(selected_rods)
#
#     current_rod = selected_rods.get(user_id, "Empty")
#     markup = create_markup_rods(current_rod)
#
#     if message_id:  # Если передан message_id, редактируем существующее сообщение
#         try:
#             bot.edit_message_text(
#                 chat_id=chat_id,
#                 message_id=message_id,
#                 text="Choose fishing rod:",
#                 reply_markup=markup
#             )
#         except Exception as e:
#             print(f"Error editing message: {e}")
#             bot.send_message(chat_id, "Choose fishing rod:", reply_markup=markup)
#     else:  # Если message_id не передан, отправляем новое сообщение
#         bot.send_message(chat_id, "Choose fishing rod:", reply_markup=markup)
#
#
# def callback_query_rods(call):
#     user_id = str(call.from_user.id)
#     button_id = call.data
#     user_money = load_money_data()
#     selected_rods = load_rods_select()
#
#     if user_id not in selected_rods:
#         selected_rods[user_id] = "Empty"
#
#     price_map = {
#         "rod1": 100,
#         "rod2": 500,
#         "rod3": 8000,
#         "rod4": 50000,
#         "rod5": 100000,
#         "rod6": 250000,
#         "rod7": 1000000,
#         "rod8": 10000000
#     }
#
#     if button_id == selected_rods.get(user_id, "Empty"):
#         # Если удочка уже выбрана, снимаем выбор
#         selected_rods[user_id] = "Empty"
#     else:
#         # Проверяем, хватает ли денег
#         price = price_map.get(button_id, 0)
#         if user_money.get(user_id, 0) >= price:
#             user_money[user_id] -= price
#             selected_rods[user_id] = button_id
#             save_money_data(user_money)
#         else:
#             bot.answer_callback_query(call.id, text="You don't have enough money(", show_alert=False)
#             return
#
#     save_state_rods(selected_rods)
#
#     updated_markup = create_markup_rods(selected_rods.get(user_id, "Empty"))
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
# def get_rods_number(rods_type):
#     if not rods_type or rods_type == "Empty":
#         return 1
#     return int(rods_type[-1]) if rods_type[-1].isdigit() else 1


import telebot
from telebot import types
import json
import os
from secrets import secrets
from logic_json import *

token = secrets.get('BOT_API_TOKEN')
bot = telebot.TeleBot(token)

JSON_FOLDER = 'json'
SAVE_FILE_RODS = os.path.join(JSON_FOLDER, 'selected_rods.json')

if os.path.exists(SAVE_FILE_RODS):
    with open(SAVE_FILE_RODS, 'r', encoding='utf-8') as f:
        selected_rods = json.load(f)
else:
    selected_rods = {}

def load_rods_select():
    if os.path.exists(SAVE_FILE_RODS):
        with open(SAVE_FILE_RODS, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

def save_state_rods(selected_rods):
    with open(SAVE_FILE_RODS, 'w', encoding='utf-8') as f:
        json.dump(selected_rods, f, ensure_ascii=False, indent=4)

def create_markup_rods(user_selected_rod):
    markup = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton(f"{'✅ ' if user_selected_rod == 'rod1' else '100$ '}Plastic rod 🎣", callback_data="rod1"),
        types.InlineKeyboardButton(f"{'✅ ' if user_selected_rod == 'rod2' else '500$ '}Improved rod 🎣", callback_data="rod2"),
        types.InlineKeyboardButton(f"{'✅ ' if user_selected_rod == 'rod3' else '8000$ '}Steel rod 🎣", callback_data="rod3"),
        types.InlineKeyboardButton(f"{'✅ ' if user_selected_rod == 'rod4' else '50000$ '}Fiberglass rod 🎣", callback_data="rod4"),
        types.InlineKeyboardButton(f"{'✅ ' if user_selected_rod == 'rod5' else '100000$ '}Heavy rod 🎣", callback_data="rod5"),
        types.InlineKeyboardButton(f"{'✅ ' if user_selected_rod == 'rod6' else '250000$ '}Alloy rod 🎣🔥", callback_data="rod6"),
        types.InlineKeyboardButton(f"{'✅ ' if user_selected_rod == 'rod7' else '1000000$ '}Lava rod 🎣🔥", callback_data="rod7"),
        types.InlineKeyboardButton(f"{'✅ ' if user_selected_rod == 'rod8' else '10000000$ '}Magma rod 🎣🔥", callback_data="rod8"),
        types.InlineKeyboardButton("back", callback_data='button_shop')
    ]
    markup.add(*buttons)
    return markup

def rods_func(chat_id, inline_message_id=None, message_id=None):
    user_id = str(chat_id)
    selected_rods = load_rods_select()

    if user_id not in selected_rods:
        selected_rods[user_id] = "Empty"
        save_state_rods(selected_rods)

    current_rod = selected_rods.get(user_id, "Empty")
    markup = create_markup_rods(current_rod)

    if inline_message_id:
        try:
            bot.edit_message_text(
                inline_message_id=inline_message_id,
                text="Choose fishing rod:",
                reply_markup=markup
            )
        except Exception as e:
            print(f"Error editing inline message: {e}")
    elif message_id:
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="Choose fishing rod:",
                reply_markup=markup
            )
        except Exception as e:
            print(f"Error editing message: {e}")
            bot.send_message(chat_id, "Choose fishing rod:", reply_markup=markup)
    else:
        bot.send_message(chat_id, "Choose fishing rod:", reply_markup=markup)

def callback_query_rods(call):
    user_id = str(call.from_user.id)
    button_id = call.data
    user_money = load_money_data()
    selected_rods = load_rods_select()

    if user_id not in selected_rods:
        selected_rods[user_id] = "Empty"

    price_map = {
        "rod1": 100, "rod2": 500, "rod3": 8000, "rod4": 50000,
        "rod5": 100000, "rod6": 250000, "rod7": 1000000, "rod8": 10000000
    }

    if button_id == selected_rods.get(user_id, "Empty"):
        selected_rods[user_id] = "Empty"
    else:
        price = price_map.get(button_id, 0)
        if user_money.get(user_id, 0) >= price:
            user_money[user_id] -= price
            selected_rods[user_id] = button_id
            save_money_data(user_money)
        else:
            bot.answer_callback_query(call.id, text="You don't have enough money(", show_alert=False)
            return

    save_state_rods(selected_rods)
    updated_markup = create_markup_rods(selected_rods.get(user_id, "Empty"))

    try:
        if hasattr(call, 'inline_message_id'):
            bot.edit_message_text(
                inline_message_id=call.inline_message_id,
                text="Choose fishing rod:",
                reply_markup=updated_markup
            )
        else:
            bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=updated_markup
            )
    except Exception as e:
        print(f"Error updating markup: {e}")

    bot.answer_callback_query(call.id)

def get_rods_number(rods_type):
    if not rods_type or rods_type == "Empty":
        return 1
    return int(rods_type[-1]) if rods_type[-1].isdigit() else 1