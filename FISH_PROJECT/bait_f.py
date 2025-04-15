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