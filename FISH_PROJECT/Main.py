from telebot import util
import telebot
import os
import json
import random
import time
import threading
from FISH_PROJECT.rods_f import load_rods_select
from secrets import secrets
from telebot import types
from fish_list import *
from logic_json import *
import rods_f
import bait_f
import boat_f
from telebot import apihelper
import sys
import select
import matplotlib
matplotlib.use('Agg')  # Важно для работы без GUI
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

# print("Текущая рабочая директория:", os.getcwd())
# print("Путь к скрипту:", os.path.dirname(os.path.abspath(__file__)))

# Глобальные переменные
last_message_id = None
user_cooldowns = {}
user_bets = {}
user_xp = load_xp_data()
selected_bait = bait_f.load_bait_select()
inline_sessions = {}
kazik_history_file = os.path.join('json', "kazik_history.json")  # Файл для истории баланса

# Инициализация бота
token = secrets.get('BOT_API_TOKEN')
bot = telebot.TeleBot(token)





# ============ INLINE HANDLERS ============
@bot.inline_handler(func=lambda query: True)
def handle_inline_query(inline_query):
    try:
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("fish", callback_data='button_fish')
        markup.add(btn1)

        result = types.InlineQueryResultArticle(
            id="1",
            title="Fishing Bot",
            description="Press to start fishing",
            input_message_content=types.InputTextMessageContent(
                message_text="Hey, {0.first_name} 👋\nTo start fishing, press fish button".format(
                    inline_query.from_user)
            ),
            reply_markup=markup
        )
        bot.answer_inline_query(inline_query.id, [result])
    except Exception as e:
        print(f"Inline query error: {e}")


# ============ CORE FUNCTIONS ============
def clean_cooldowns():
    while True:
        current_time = time.time()
        for user_id in list(user_cooldowns.keys()):
            if current_time - user_cooldowns[user_id] > 600:
                del user_cooldowns[user_id]
        time.sleep(1800)


cleanup_thread = threading.Thread(target=clean_cooldowns)
cleanup_thread.daemon = True
cleanup_thread.start()

# ============ KAZIK HISTORY FUNCTIONS ============
# ============ KAZIK HISTORY FUNCTIONS ============
def load_kazik_history():
    """Загружаем историю баланса Kazik_Bank"""
    try:
        with open(kazik_history_file, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_kazik_history(history):
    """Сохраняем историю баланса Kazik_Bank"""
    with open(kazik_history_file, 'w') as f:
        json.dump(history, f)

def update_kazik_history(balance):
    """Обновляем историю баланса"""
    history = load_kazik_history()

    # Ограничиваем историю 1000 последними записями
    if len(history) >= 1000:
        history = history[-999:]

    history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "balance": balance
    })

    save_kazik_history(history)
# ============ STAT COMMAND HANDLER ============
@bot.message_handler(commands=['stat'])
def handle_stat_command(message):
    """Обработчик команды stat для показа графика баланса"""
    history = load_kazik_history()

    if not history:
        bot.reply_to(message, "История баланса казика пустая.")
        return

    # Подготовка данных для графика
    changes = list(range(1, len(history) + 1))
    balances = [point["balance"] for point in history]
    current_balance = balances[-1] if balances else 0

    # Создаем график с улучшенной визуализацией
    plt.figure(figsize=(12, 6))

    # Основная линия графика
    plt.plot(changes, balances, linestyle='-', color='#1f77b4', linewidth=2, alpha=0.8)

    # Точки для важных изменений
    plt.scatter(changes, balances, color='#ff7f0e', s=15, alpha=0.6)

    # Добавляем горизонтальную линию для текущего баланса
    plt.axhline(y=current_balance, color='g', linestyle='--', alpha=0.5)

    # Заголовки и подписи
    plt.title(f'История баланса Kazik Bank\nТекущий баланс: {current_balance}$', fontsize=14)
    plt.xlabel('Количество игр в coinflip', fontsize=12)
    plt.ylabel('Баланс ($)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)

    # Автоматическое масштабирование
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Сохраняем график во временный файл
    temp_file = "kazik_stat.png"
    plt.savefig(temp_file, dpi=150)  # Увеличиваем разрешение
    plt.close()

    # Создаем HTML-версию с улучшенной визуализацией
    html_content = f"""
    <html>
    <head>
        <title>История баланса Kazik Bank</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            .stats {{ margin-top: 20px; }}
            .stats-table {{ width: 100%; border-collapse: collapse; }}
            .stats-table th, .stats-table td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
            .stats-table tr:hover {{ background-color: #f5f5f5; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>История баланса Kazik Bank</h1>
            <div id="plot"></div>

            <div class="stats">
                <h2>Статистика</h2>
                <table class="stats-table">
                    <tr>
                        <th>Текущий баланс:</th>
                        <td>{current_balance}$</td>
                    </tr>
                    <tr>
                        <th>Всего игр:</th>
                        <td>{len(history)}</td>
                    </tr>
                    <tr>
                        <th>Максимальный баланс:</th>
                        <td>{max(balances) if balances else 0}$</td>
                    </tr>
                    <tr>
                        <th>Минимальный баланс:</th>
                        <td>{min(balances) if balances else 0}$</td>
                    </tr>
                    <tr>
                        <th>Средний баланс:</th>
                        <td>{sum(balances) / len(balances) if balances else 0:.2f}$</td>
                    </tr>
                </table>
            </div>
        </div>

        <script>
            var data = [{{
                x: {changes},
                y: {balances},
                type: 'scatter',
                mode: 'lines+markers',
                marker: {{ color: '#1f77b4', size: 4 }},
                line: {{ width: 2 }},
                name: 'Баланс'
            }}];

            var layout = {{
                title: 'Динамика баланса Kazik Bank',
                xaxis: {{ title: 'Количество игр в coinflip' }},
                yaxis: {{ title: 'Баланс ($)' }},
                hovermode: 'closest',
                showlegend: false
            }};

            Plotly.newPlot('plot', data, layout);
        </script>
    </body>
    </html>
    """

    # Сохраняем HTML во временный файл
    html_file = "kazik_stat.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # Отправляем пользователю оба варианта
    with open(temp_file, 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption="График баланса Kazik_Bank")

    with open(html_file, 'rb') as html:
        bot.send_document(message.chat.id, html, caption="html версия")

    # Удаляем временные файлы
    os.remove(temp_file)
    os.remove(html_file)


@bot.callback_query_handler(func=lambda call: call.data == 'stats_menu')
def handle_stats_menu(call):
    user_money = load_money_data()

    # Создаем список пользователей, исключая Kazik_Bank
    users_list = []
    for user_id, money in user_money.items():
        if user_id == "Kazik_Bank":
            continue
        users_list.append((user_id, money))

    # Сортируем по убыванию денег
    users_list.sort(key=lambda x: x[1], reverse=True)

    # Формируем текст сообщения
    text = "💰 Top 10 Users by Money:\n\n"

    # Всегда добавляем Kazik_Bank первым
    text += f"0. Kazik_Bank: {user_money.get('Kazik_Bank', 0)}$\n"

    # Добавляем топ-10 пользователей
    for i, (user_id, money) in enumerate(users_list[:10], start=1):
        try:
            # Пытаемся получить имя пользователя по ID
            user_info = bot.get_chat(user_id)
            name = user_info.first_name
        except:
            name = f"User {user_id}"
        text += f"{i}. {name}: {money}$\n"

    # Создаем клавиатуру с кнопкой "Back"
    markup = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton("Back", callback_data='button_menu')
    markup.add(btn_back)

    # Редактируем сообщение
    if hasattr(call, 'inline_message_id'):
        bot.edit_message_text(
            inline_message_id=call.inline_message_id,
            text=text,
            reply_markup=markup
        )
    else:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=markup
        )


def menu_button(chat_id, inline_message_id=None):
    global last_message_id

    user_id = str(chat_id)
    user_bait_data = load_bait_data()

    # Добавляем кнопки
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("Shop 🪱", callback_data='button_shop')
    btn2 = types.InlineKeyboardButton("Fishing 🎣", callback_data='sub_button_menu')
    btn3 = types.InlineKeyboardButton("Coinflip 🎰", callback_data='coinflip_menu')
    btn4 = types.InlineKeyboardButton("Stats 📊", callback_data='stats_menu')
    markup.add(btn2, btn1, btn3, btn4)

    selected_bait = bait_f.load_bait_select()
    user_money = load_money_data()
    user_xp = load_xp_data()

    # Получаем данные уровня
    current_xp = user_xp.get(user_id, 0)
    current_level = calculate_level(current_xp)
    color = get_level_color(current_level)
    next_level_xp = get_xp_for_next_level(current_level)
    progress = get_level_progress(current_xp)
    progress_bar = create_progress_bar(progress)

    # Формируем текст с прогрессом уровня
    # {progress_bar} {progress}%
    text = f"""Menu:
Balance: {user_money.get(user_id, 0)}$
Level: {current_level} {color}
{progress_bar} {progress}%
XP: {current_xp} | Next: {next_level_xp} XP

Bait: {selected_bait.get(user_id, "Empty")} {user_bait_data.get(user_id, {}).get(selected_bait.get(user_id, "Empty"), 0)}"""

    if inline_message_id:
        bot.edit_message_text(
            inline_message_id=inline_message_id,
            text=text,
            reply_markup=markup
        )
    elif last_message_id:
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=last_message_id,
                text=text,
                reply_markup=markup
            )
        except:
            msg = bot.send_message(chat_id, text, reply_markup=markup)
            last_message_id = msg.message_id
    else:
        msg = bot.send_message(chat_id, text, reply_markup=markup)
        last_message_id = msg.message_id


@bot.callback_query_handler(func=lambda call: call.data == 'coinflip_menu')
def handle_coinflip_menu(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_heads = types.InlineKeyboardButton("Heads", callback_data='coinflip_heads')
    btn_tails = types.InlineKeyboardButton("Tails", callback_data='coinflip_tails')
    btn_back = types.InlineKeyboardButton("Back", callback_data='button_menu')
    markup.add(btn_heads, btn_tails, btn_back)

    try:
        if hasattr(call, 'inline_message_id'):
            bot.edit_message_text(
                inline_message_id=call.inline_message_id,
                text="Choose Heads or Tails:",
                reply_markup=markup
            )
        else:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Choose Heads or Tails:",
                reply_markup=markup
            )
    except Exception as e:
        print(f"Error editing message: {e}")


@bot.callback_query_handler(func=lambda call: call.data.startswith('coinflip_'))
def handle_coinflip_actions(call):
    user_id = str(call.from_user.id)

    # Обработка выбора "Heads" или "Tails"
    if call.data in ['coinflip_heads', 'coinflip_tails']:
        choice = call.data.split('_')[1]
        user_bets[user_id] = {'choice': choice}

        markup = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton("Back", callback_data='coinflip_menu')
        btn_20 = types.InlineKeyboardButton("20% of balance", callback_data='coinflip_bet_20')
        btn_50 = types.InlineKeyboardButton("50% of balance", callback_data='coinflip_bet_50')
        btn_100 = types.InlineKeyboardButton("100% of balance", callback_data='coinflip_bet_100')
        markup.add(btn_20, btn_50, btn_100, btn_back)

        bot.edit_message_text(
            inline_message_id=call.inline_message_id if hasattr(call, 'inline_message_id') else None,
            chat_id=None if hasattr(call, 'inline_message_id') else call.message.chat.id,
            message_id=None if hasattr(call, 'inline_message_id') else call.message.message_id,
            text=f"You chose {choice.capitalize()}. Now choose the bet amount:",
            reply_markup=markup
        )

    # Обработка ставки (20%, 50%, 100%)
    elif call.data.startswith('coinflip_bet_'):
        if user_id not in user_bets:
            bot.answer_callback_query(call.id, "❌ Error: Choice not found. Start again.")
            return

        user_money = load_money_data()
        current_money = user_money.get(user_id, 0)
        choice = user_bets[user_id]['choice']

        # Определяем ставку
        percent = int(call.data.split('_')[2])  # 20, 50, 100
        bet = int(current_money * (percent / 100))

        if bet <= 0:
            bot.answer_callback_query(call.id, "❌ Your balance is too low!")
            return

        # Подбрасываем монету
        result = random.choice(['heads', 'tails'])
        win = choice == result

        # Обновляем баланс
        user_money[user_id] = current_money + (bet if win else -bet)
        user_money['Kazik_Bank'] += (-bet if win else bet)

        save_money_data(user_money)

        update_kazik_history(user_money['Kazik_Bank'])

        # Формируем результат
        result_text = (
            f"🪙 Coin flip result: {result.capitalize()}!\n"
            f"Your choice: {choice.capitalize()}\n"
            f"Bet: {bet}$\n\n"
            f"{'🎉 You won!' if win else '😢 You lost...'} {'+' if win else '-'}{bet}$\n"
            f"Balance: {user_money[user_id]}$"
        )

        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_again = types.InlineKeyboardButton("Play again", callback_data='coinflip_menu')
        btn_back = types.InlineKeyboardButton("Back to menu", callback_data='button_menu')
        markup.add(btn_again, btn_back)

        # Отправляем результат
        if hasattr(call, 'inline_message_id'):
            bot.edit_message_text(
                inline_message_id=call.inline_message_id,
                text=result_text,
                reply_markup=markup
            )
        else:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=result_text,
                reply_markup=markup
            )

    # Обработка возврата в меню
    elif call.data == 'coinflip_menu':
        handle_coinflip_menu(call)





@bot.callback_query_handler(func=lambda call: call.data == 'rod')
def handle_rod_callback(call):
    if hasattr(call, 'inline_message_id'):
        rods_f.rods_func(call.from_user.id, inline_message_id=call.inline_message_id)
    else:
        rods_f.rods_func(call.message.chat.id, message_id=call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data == 'boat')
def handle_boat_callback(call):
    if hasattr(call, 'inline_message_id'):
        boat_f.boat_func(call.from_user.id, inline_message_id=call.inline_message_id)
    else:
        boat_f.boat_func(call.message.chat.id, message_id=call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data == 'bait')
def handle_bait_callback(call):
    if hasattr(call, 'inline_message_id'):
        bait_f.bait_func(call.from_user.id, inline_message_id=call.inline_message_id)
    else:
        bait_f.bait_func(call.message.chat.id, message_id=call.message.message_id)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    global last_message_id

    user_id = str(call.from_user.id)
    inline_msg_id = call.inline_message_id if hasattr(call, 'inline_message_id') else None

    # Инициализация данных пользователя (остается без изменений)
    user_money = load_money_data()
    user_xp = load_xp_data()
    if user_id not in user_money:
        user_money[user_id] = 0
        save_money_data(user_money)
    if user_id not in user_xp:
        user_xp[user_id] = 0
        save_xp_data(user_xp)

    user_bait_data = load_bait_data()
    if user_id not in user_bait_data:
        user_bait_data[user_id] = {
            "Empty": 0,
            "Worms": 0,
            "Leeches": 0,
            "Magnet": 0
        }
        save_bait_data(user_bait_data)

    selected_bait = bait_f.load_bait_select()
    if user_id not in selected_bait:
        selected_bait[user_id] = "Empty"
        bait_f.save_state_bait(selected_bait)

    biome = load_biome_data()
    if user_id not in biome:
        biome[user_id] = "River"
    save_biome_data(biome)

    boat = boat_f.load_boat_select()
    if user_id not in boat:
        boat[user_id] = "Empty"
        boat_f.save_state_boat(boat)

    selected_rods = rods_f.load_rods_select()
    if user_id not in selected_rods:
        selected_rods[user_id] = "Empty"
        rods_f.save_state_rods(selected_rods)

    # Обработка callback данных
    if call.data == 'button_fish':
        user_money[user_id] += fish_price1()
        save_money_data(user_money)


        bait_type = selected_bait[user_id]
        if user_bait_data[user_id][bait_type] > 0:
            user_bait_data[user_id][bait_type] -= 1
        else:
            bot.answer_callback_query(call.id, text="You out of baits", show_alert=False)
            selected_bait[user_id] = "Empty"
        bait_f.save_state_bait(selected_bait)
        save_bait_data(user_bait_data)

        bot.answer_callback_query(call.id, text="+" + str(fish_price1()) + "$", show_alert=False)
        fish_menu(call)

    elif call.data == 'button_menu':
        menu_button(call.from_user.id, inline_msg_id)
    elif call.data == 'sub_btn_fish':
        fish_menu(call)
    elif call.data == 'sub_button_menu':
        fish_menu(call)
    elif call.data == 'button_shop':
        shop_button(call.from_user.id, inline_msg_id)
    elif call.data == 'button_back':
        menu_button(call.from_user.id, inline_msg_id)
    elif call.data == 'rod':
        rods_f.rods_func(call.from_user.id, inline_msg_id if inline_msg_id else call.message.message_id)
    elif call.data in ["rod1", 'rod2', 'rod3', "rod4", 'rod5', 'rod6', 'rod7', 'rod8']:
        rods_f.callback_query_rods(call)
    elif call.data == 'boat':
        boat_f.boat_func(call.from_user.id, inline_msg_id if inline_msg_id else call.message.message_id)
    elif call.data in ["boat1", 'boat2', 'boat3', "boat4", 'boat5', 'boat6']:
        boat_f.callback_query_boat(call)
    # elif call.data == 'bait':
    #     bait_f.bait_func(call.from_user.id, inline_msg_id if inline_msg_id else call.message.message_id)

    # elif call.data == 'Worms':
    #     if selected_bait[user_id] in ["Worms"]:
    #         bait_f.save_state_bait(selected_bait)
    #         bait_f.callback_query_bait(call)
    #         user_bait_data = load_bait_data()
    #         user_bait_data[user_id]["Worms"] += 20
    #         save_bait_data(user_bait_data)
    #         return
    #
    #     if user_money[user_id] >= 80:
    #         user_money[user_id] -= 80
    #         save_money_data(user_money)
    #         bait_type = "Worms"
    #         selected_bait[user_id] = bait_f.load_bait_select()
    #         user_bait_data = load_bait_data()
    #         if (bait_type not in selected_bait[user_id]) and (user_bait_data[user_id]["Worms"] > 0):
    #             selected_bait[user_id] = "Empty"
    #             bait_f.save_state_bait(selected_bait)
    #             bait_f.callback_query_bait(call)
    #         else:
    #             selected_bait[user_id] = "Worms"
    #             bait_f.save_state_bait(selected_bait)
    #             bait_f.callback_query_bait(call)
    #             user_bait_data[user_id][bait_type] = 20
    #             save_bait_data(user_bait_data)
    #         save_bait_data(user_bait_data)
    #     elif user_bait_data[user_id]["Worms"] > 0:
    #         bait_f.callback_query_bait(call)
    #     else:
    #         bot.answer_callback_query(call.id, text="You don't have enough money(", show_alert=False)
    # elif call.data == 'Leeches':
    #     if selected_bait[user_id] in ["Leeches"]:
    #         bait_f.save_state_bait(selected_bait)
    #         bait_f.callback_query_bait(call)
    #         user_bait_data = load_bait_data()
    #         user_bait_data[user_id]["Leeches"] += 20
    #         save_bait_data(user_bait_data)
    #         return
    #
    #     if user_money[user_id] >= 500:
    #         user_money[user_id] -= 500
    #         save_money_data(user_money)
    #         bait_type = "Leeches"
    #         selected_bait[user_id] = bait_f.load_bait_select()
    #         user_bait_data = load_bait_data()
    #         if (bait_type not in selected_bait[user_id]) and (user_bait_data[user_id]["Leeches"] > 0):
    #             selected_bait[user_id] = "Empty"
    #             bait_f.save_state_bait(selected_bait)
    #             bait_f.callback_query_bait(call)
    #         else:
    #             selected_bait[user_id] = "Leeches"
    #             bait_f.save_state_bait(selected_bait)
    #             bait_f.callback_query_bait(call)
    #             user_bait_data[user_id][bait_type] = 20
    #             save_bait_data(user_bait_data)
    #         save_bait_data(user_bait_data)
    #     elif user_bait_data[user_id]["Leeches"] > 0:
    #         bait_f.callback_query_bait(call)
    #     else:
    #         bot.answer_callback_query(call.id, text="You don't have enough money(", show_alert=False)
    # elif call.data == 'Magnet':
    #     if selected_bait[user_id] in ["Magnet"]:
    #         bait_f.save_state_bait(selected_bait)
    #         bait_f.callback_query_bait(call)
    #         user_bait_data = load_bait_data()
    #         user_bait_data[user_id]["Magnet"] += 20
    #         save_bait_data(user_bait_data)
    #         return
    #
    #     if user_money[user_id] >= 500:
    #         user_money[user_id] -= 500
    #         save_money_data(user_money)
    #         bait_type = "Magnet"
    #         selected_bait[user_id] = bait_f.load_bait_select()
    #         user_bait_data = load_bait_data()
    #         if (bait_type not in selected_bait[user_id]) and (user_bait_data[user_id]["Magnet"] > 0):
    #             selected_bait[user_id] = "Empty"
    #             bait_f.save_state_bait(selected_bait)
    #             bait_f.callback_query_bait(call)
    #         else:
    #             selected_bait[user_id] = "Magnet"
    #             bait_f.save_state_bait(selected_bait)
    #             bait_f.callback_query_bait(call)
    #             user_bait_data[user_id][bait_type] = 20
    #             save_bait_data(user_bait_data)
    #         save_bait_data(user_bait_data)
    #     elif user_bait_data[user_id]["Magnet"] > 0:
    #         bait_f.callback_query_bait(call)
    #     else:
    #         bot.answer_callback_query(call.id, text="You don't have enough money(", show_alert=False)
    elif call.data in ['Worms', 'Leeches', 'Magnet']:
        bait_f.callback_query_bait(call)
        return  # Важно! Чтобы не было двойного answer_callback_query
    bot.answer_callback_query(call.id)


# ============ LEVEL SYSTEM ============
def calculate_level(xp):
    """Calculate level based on exponential formula"""
    if xp < 100:
        return 0
    return int((xp / 100) ** 0.5)


def get_level_color(level):
    """Get color symbol based on level"""
    colors = ['🟤', '🟣', '🔵', '🟢', '🟡', '🟠', '🔴', '⚪', '⚫']
    if level < 10:
        return colors[0]
    elif level < 20:
        return colors[1]
    elif level < 30:
        return colors[2]
    elif level < 40:
        return colors[3]
    elif level < 50:
        return colors[4]
    elif level < 75:
        return colors[5]
    elif level < 100:
        return colors[6]
    elif level < 120:
        return colors[7]
    else:
        return colors[8]


def get_xp_for_next_level(current_level):
    """Calculate XP needed for next level"""
    return (current_level + 1) ** 2 * 100


def get_level_progress(current_xp):
    """Get progress to next level"""
    current_level = calculate_level(current_xp)
    next_level_xp = get_xp_for_next_level(current_level)
    current_level_xp = (current_level ** 2) * 100

    # Calculate progress percentage
    progress = (current_xp - current_level_xp) / (next_level_xp - current_level_xp) * 100
    return min(100, max(0, int(progress)))  # Clamp between 0-100


def create_progress_bar(progress):
    """Create visual progress bar"""
    bar_length = 10
    filled = int(progress / 100 * bar_length)
    return '=' * filled + '-' * (bar_length - filled)



def fish_menu(call):
    global last_message_id
    user_xp = load_xp_data()
    current_time = time.time()
    user_id = str(call.from_user.id)

    if user_id in user_cooldowns:
        last_request_time = user_cooldowns[user_id]
        if current_time - last_request_time < 3:
            bot.answer_callback_query(call.id, "You must wait 3s before performing this action again.", show_alert=True)
            return
    user_cooldowns[user_id] = current_time

    selected_rods = rods_f.load_rods_select()
    selected_bait = bait_f.load_bait_select()
    boat_data = boat_f.load_boat_select()
    current_rod = selected_rods.get(user_id, "Empty")
    current_bait = selected_bait.get(user_id, "Empty")
    current_boat = boat_data.get(user_id, "Empty")

    rod_number = rods_f.get_rods_number(current_rod)
    bait_number = bait_f.get_bait_number(current_bait)
    boat_number = boat_f.get_boat_number(current_boat)
    fMAX = int(((rod_number ** 1.3) + (bait_number * 4) + random.choice([-1, -2, 1, 2, 3, 4, 5, 6, 3, 2, 3]) + (
                boat_number * 20))+1//1.3)

    temp_money = 0
    temp_xp = 0
    fish_list = []

    if current_rod in ['Empty', 'rod1', 'rod2']:
        temp_fishlist = random.choice(T1)
        if isinstance(temp_fishlist, tuple):
            for _ in range(abs(fMAX - 16)):
                temp_fish = random.choice(temp_fishlist)
                parts = temp_fish.split()
                temp_money += int(parts[0])
                temp_xp += int(parts[1])
                fish_list.append(parts[2])
            if bait_number == 2:
                if random.randint(1, 2) == 2:
                    CHparts = ChestT1.split()
                    temp_money += int(CHparts[0])
                    temp_xp += int(CHparts[1])
                    fish_list.append(CHparts[2])
                fish_list = sorted(fish_list)
            if random.randint(1, 2) == 2:
                CHparts = ChestT1.split()
                temp_money += int(CHparts[0])
                temp_xp += int(CHparts[1])
                fish_list.append(CHparts[2])
            fish_list = sorted(fish_list)
        else:
            for _ in range(abs(fMAX - 16)):
                temp_fish = temp_fishlist
                parts = temp_fish.split()
                temp_money += int(parts[0])
                temp_xp += int(parts[1])
                fish_list.append(parts[2])

    elif current_rod in ['rod3']:
        temp_fishlist = random.choice(T2)
        if isinstance(temp_fishlist, tuple):
            for _ in range(abs(fMAX - 5)):
                temp_fish = random.choice(temp_fishlist)
                parts = temp_fish.split()
                temp_money += int(parts[0])
                temp_xp += int(parts[1])
                fish_list.append(parts[2])
            if random.randint(1, 18) <= 3:
                CHparts = ChestT2.split()
                temp_money += int(CHparts[0])
                temp_xp += int(CHparts[1])
                fish_list.append(CHparts[2])
            if bait_number == 2:
                if random.randint(1, 5) == 2:
                    CHparts = ChestT3.split()
                    temp_money += int(CHparts[0])
                    temp_xp += int(CHparts[1])
                    fish_list.append(CHparts[2])
                fish_list = sorted(fish_list)
            elif random.randint(1, 25) == 10:
                CHparts = ChestT3.split()
                temp_money += int(CHparts[0])
                temp_xp += int(CHparts[1])
                fish_list.append(CHparts[2])
            fish_list = sorted(fish_list)
        else:
            for _ in range(abs(fMAX - 10)):
                temp_fish = temp_fishlist
                parts = temp_fish.split()
                temp_money += int(parts[0])
                temp_xp += int(parts[1])
                fish_list.append(parts[2])
            if random.randint(1, 100) <= 15:
                CHparts = ChestT2.split()
                temp_money += int(CHparts[0])
                temp_xp += int(CHparts[1])
                fish_list.append(CHparts[2])

    elif current_rod in ['rod4']:
        temp_fishlist = random.choice(T3)
        if isinstance(temp_fishlist, tuple):
            for _ in range(abs(fMAX - 5)):
                temp_fish = random.choice(temp_fishlist)
                parts = temp_fish.split()
                temp_money += int(parts[0])
                temp_xp += int(parts[1])
                fish_list.append(parts[2])
            if bait_number == 2:
                if random.randint(1, 100) <= 40:
                    CHparts = ChestT3.split()
                    temp_money += int(CHparts[0])
                    temp_xp += int(CHparts[1])
                    fish_list.append(CHparts[2])
            if random.randint(1, 100) <= 10:
                CHparts = ChestT2.split()
                temp_money += int(CHparts[0])
                temp_xp += int(CHparts[1])
                fish_list.append(CHparts[2])
                fish_list = sorted(fish_list)
            if bait_number == 2:
                if random.randint(1, 100) <= 40:
                    CHparts = ChestT3.split()
                    temp_money += int(CHparts[0])
                    temp_xp += int(CHparts[1])
                    fish_list.append(CHparts[2])
                fish_list = sorted(fish_list)
            elif random.randint(1, 65) == 1:
                CHparts = ChestT4.split()
                temp_money += int(CHparts[0])
                temp_xp += int(CHparts[1])
                fish_list.append(CHparts[2])
            fish_list = sorted(fish_list)
        else:
            for _ in range(abs(fMAX - 5)):
                temp_fish = temp_fishlist
                parts = temp_fish.split()
                temp_money += int(parts[0])
                temp_xp += int(parts[1])
                fish_list.append(parts[2])
                fish_list = sorted(fish_list)

    elif current_rod in ['rod5']:
        temp_fishlist = random.choice(T4)
        if isinstance(temp_fishlist, tuple):
            for _ in range(abs(fMAX - 5)):
                temp_fish = random.choice(temp_fishlist)
                parts = temp_fish.split()
                temp_money += int(parts[0])
                temp_xp += int(parts[1])
                fish_list.append(parts[2])
            if random.randint(1, 100) <= 7:
                CHparts = ChestT3.split()
                temp_money += int(CHparts[0])
                temp_xp += int(CHparts[1])
                fish_list.append(CHparts[2])
            if bait_number == 2:
                if random.randint(1, 100) <= 40:
                    CHparts = ChestT4.split()
                    temp_money += int(CHparts[0])
                    temp_xp += int(CHparts[1])
                    fish_list.append(CHparts[2])
            elif random.randint(1, 80) == 1:
                CHparts = ChestT2.split()
                temp_money += int(CHparts[0])
                temp_xp += int(CHparts[1])
                fish_list.append(CHparts[2])
            fish_list = sorted(fish_list)

        else:
            for _ in range(abs(fMAX - 5)):
                if bait_number == 2:
                    if random.randint(1, 120) == 2:
                        CHparts = ChestT3.split()
                        temp_money += int(CHparts[0])
                        temp_xp += int(CHparts[1])
                        fish_list.append(CHparts[2])
                temp_fish = temp_fishlist
                parts = temp_fish.split()
                temp_money += int(parts[0])
                temp_xp += int(parts[1])
                fish_list.append(parts[2])
                fish_list = sorted(fish_list)
    elif current_rod in ['rod6', 'rod7', 'rod8']:
        temp_fishlist = random.choice(LT1)
        if isinstance(temp_fishlist, tuple):
            for _ in range(abs(fMAX - 5)):
                temp_fish = random.choice(temp_fishlist)
                parts = temp_fish.split()
                temp_money += int(parts[0])
                temp_xp += int(parts[1])
                fish_list.append(parts[2])
            if bait_number == 2:
                if random.randint(1, 100) <= 30:
                    CHparts = ChestT4.split()
                    temp_money += int(CHparts[0])
                    temp_xp += int(CHparts[1])
                    fish_list.append(CHparts[2])
            if random.randint(1, 120) <= 10:
                CHparts = ChestT4.split()
                temp_money += int(CHparts[0])
                temp_xp += int(CHparts[1])
                fish_list.append(CHparts[2])
            if bait_number == 2:
                if random.randint(1, 100) <= 20:
                    CHparts = ChestT4.split()
                    temp_money += int(CHparts[0])
                    temp_xp += int(CHparts[1])
                    fish_list.append(CHparts[2])
                fish_list = sorted(fish_list)
            elif random.randint(1, 100) == 1:
                CHparts = ChestT5.split()
                temp_money += int(CHparts[0])
                temp_xp += int(CHparts[1])
                fish_list.append(CHparts[2])
            fish_list = sorted(fish_list)
            fish_list = sorted(fish_list)
        else:
            for _ in range(abs(fMAX - 5)):
                temp_fish = temp_fishlist
                parts = temp_fish.split()
                temp_money += int(parts[0])
                temp_xp += int(parts[1])
                fish_list.append(parts[2])
            if random.randint(1, 100) <= 10:
                CHparts = ChestT3.split()
                temp_money += int(CHparts[0])
                temp_xp += int(CHparts[1])
                fish_list.append(CHparts[2])
            fish_list = sorted(fish_list)

    user_money = load_money_data()
    user_xp = load_xp_data()
    user_money[user_id] += temp_money
    save_money_data(user_money)

    user_xp[user_id] += temp_xp
    save_xp_data(user_xp)

    # Добавляем расчет уровня и цвета
    current_xp = user_xp[user_id]
    level = calculate_level(current_xp)
    color = get_level_color(level)

    fish_counts = {fish: fish_list.count(fish) for fish in set(fish_list)}
    message_text = f"{call.from_user.first_name} {color}\nLevel: {level}\n\nYou caught:\n"
    for fish, count in fish_counts.items():
        message_text += f"x{count} {fish}\n"
    message_text += f"\n +{temp_money}$\n +{temp_xp} XP"

    user_bait_data = load_bait_data()
    if user_bait_data[user_id].get(current_bait, 0) > 0:
        user_bait_data[user_id][current_bait] -= 1
        save_bait_data(user_bait_data)
    else:
        bot.answer_callback_query(call.id, "You're out of baits!", show_alert=False)
        selected_bait[user_id] = "Empty"
        bait_f.save_state_bait(selected_bait)

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("fish again 🎣", callback_data='sub_btn_fish'),
        types.InlineKeyboardButton("menu", callback_data='button_menu')
    )


    if hasattr(call, 'inline_message_id'):
        bot.edit_message_text(
            inline_message_id=call.inline_message_id,
            text=message_text,
            reply_markup=markup
        )
    else:
        msg = bot.send_message(call.message.chat.id, message_text, reply_markup=markup)
        last_message_id = msg.message_id



def shop_button(chat_id, inline_message_id=None):
    global last_message_id

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("fishing rod", callback_data='rod')
    btn4 = types.InlineKeyboardButton("boats", callback_data='boat')
    btn2 = types.InlineKeyboardButton("baits", callback_data='bait')
    btn3 = types.InlineKeyboardButton("back", callback_data='button_back')
    markup.add(btn1, btn4, btn2, btn3)

    user_id = str(chat_id)
    user_money = load_money_data()
    user_xp = load_xp_data()

    text = f"Shop: \n  Balance: {user_money[user_id]}"

    if inline_message_id:
        bot.edit_message_text(
            inline_message_id=inline_message_id,
            text=text,
            reply_markup=markup
        )
    elif last_message_id:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=last_message_id,
            text=text,
            reply_markup=markup
        )
    else:
        msg = bot.send_message(chat_id, text, reply_markup=markup)
        last_message_id = msg.message_id

    save_money_data(user_money)



@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Bot running🎣💕\nMention @VirtualFisherBot in any chat to start fishing, enjoy")



def check_input():
    while True:
        try:
            cmd = input().strip()
            if cmd == "fish_stop":
                print("Остановка по коду 1488")
                os._exit(0)  # Мгновенный выход

                # ========== ОБЩИЕ КОМАНДЫ ==========
            elif cmd == "fish_list":
                user_money = load_money_data()
                user_xp = load_xp_data()

                all_users = set(user_money.keys()) | set(user_xp.keys())

                if not all_users:
                    print("📝 Пользователей не найдено")
                else:
                    print("📝 Список всех пользователей:")
                    for user_id in sorted(all_users):
                        money = user_money.get(user_id, 0)
                        xp = user_xp.get(user_id, 0)

                        try:
                            # Пытаемся получить имя пользователя по ID
                            user_info = bot.get_chat(user_id)
                            name = user_info.first_name
                        except:
                            name = f"User {user_id}"

                        print(f"   👤 {user_id} {name}: {money}$ | {xp} XP")




            elif cmd == "fish_reset_user":
                print("Введите ID пользователя для сброса данных:")
                user_id = input().strip()

                if not user_id:
                    print("❌ Ошибка: ID пользователя не может быть пустым")
                    continue

                print("⚠️  ВНИМАНИЕ! Это действие удалит ВСЕ данные пользователя:")
                print(f"   -прогресс")
                print("ГОООЛ? (да/нет):")

                confirm = input().strip().lower()
                if confirm in ['да', 'yes', 'y']:
                    # Сброс денег
                    user_money = load_money_data()
                    if user_id in user_money:
                        del user_money[user_id]
                        save_money_data(user_money)

                    # Сброс XP
                    user_xp = load_xp_data()
                    if user_id in user_xp:
                        user_xp[user_id] = 0
                        del user_xp[user_id]
                        save_xp_data(user_xp)

                    # Сброс наживки
                    user_bait_data = load_bait_data()
                    if user_id in user_bait_data:
                        del user_bait_data[user_id]
                        save_bait_data(user_bait_data)

                    # Сброс выбранной наживки
                    selected_bait = bait_f.load_bait_select()
                    if user_id in selected_bait:
                        del selected_bait[user_id]
                        bait_f.save_state_bait(selected_bait)

                    # Сброс удочки
                    user_rods_data = load_rods_select()
                    if user_id in user_rods_data:
                        del user_rods_data[user_id]
                        rods_f.save_state_rods(user_bait_data)

                    # Сброс выбранной удочки
                    selected_rods = rods_f.load_rods_select()
                    if user_id in selected_rods:
                        del selected_rods[user_id]
                        rods_f.save_state_rods(selected_bait)

                    # Сброс лодки
                    user_boat_data = boat_f.load_boat_select()
                    if user_id in user_boat_data:
                        del user_boat_data[user_id]
                        boat_f.save_state_boat(user_bait_data)


                    print(f"✅ Все данные пользователя {user_id} успешно сброшены")
                else:
                    print("❌ Операция отменена")

            elif cmd == "fish_user":
                print("Введите ID пользователя для просмотра:")
                user_id = input().strip()
                user_money = load_money_data()
                user_xp = load_xp_data()
                user_bait_data = load_bait_data()
                selected_bait = bait_f.load_bait_select()
                user_rods_data = load_rods_select()
                selected_rods = rods_f.load_rods_select()
                user_boat_data = boat_f.load_boat_select()
                try:
                    # Пытаемся получить имя пользователя по ID
                    user_info = bot.get_chat(user_id)
                    name = user_info.first_name
                except:
                    name = f"User {user_id}"

                print(f"👤 {user_id} {name}:"
                      f"\n{user_money[user_id]}$ "
                      f"\n{user_xp[user_id]}XP "
                      f"\n{calculate_level(user_xp[user_id])}lvl "
                      f"\nBAITS| {user_bait_data[user_id]}"
                      f"\nCURRENT_BAIT| {selected_bait[user_id]}"
                      f"\nRODS| {user_rods_data[user_id]}"
                      f"\nCURRENT_ROD| {selected_rods[user_id]}"
                      f"\nBOAT| {user_boat_data[user_id]}"
                      )



            elif cmd == "fish_help":
                print("📋 Доступные команды:")
                print("\n💰 ДЕНЬГИ:")
                print("  fish_add_money - добавить деньги пользователю")
                print("  fish_check_money - проверить баланс пользователя")
                print("\n⭐ ОПЫТ (XP):")
                print("  fish_add_xp - добавить XP пользователю")
                print("  fish_check_xp - проверить XP пользователя")
                print("\n🔧 УПРАВЛЕНИЕ:")
                print("  fish_list - показать всех пользователей")
                print("  fish_reset_user - сбросить все данные пользователя")
                print("  fish_stop - остановка бота")
                print("  fish_help - показать эту справку")

# ========== КОМАНДЫ ДЛЯ BABLO =======================================================================================
            elif cmd == "fish_add_money":
                print("Введите ID пользователя:")
                user_id = input().strip()

                if not user_id:
                    print("❌ Ошибка: ID пользователя не может быть пустым")
                    continue

                print("Введите сумму для добавления:")
                amount = int(input().strip())
                # Загружаем данные о деньгах
                user_money = load_money_data()
                # Добавляем деньги пользователю
                if user_id not in user_money:
                    user_money[user_id] = 0

                old_amount = user_money[user_id]
                user_money[user_id] += amount
                # Сохраняем данные
                save_money_data(user_money)

                print(f"✅ Добавлено {amount}$ пользователю {user_id}")
                print(f"   Было: {old_amount}$ → Стало: {user_money[user_id]}$")

            elif cmd == "fish_check_money":
                print("Введите ID пользователя для проверки баланса:")
                user_id = input().strip()

                if not user_id:
                    print("❌ Ошибка: ID пользователя не может быть пустым")
                    continue

                user_money = load_money_data()
                balance = user_money.get(user_id, 0)
                print(f"💰 Баланс пользователя {user_id}: {balance}$")

# ========== КОМАНДЫ ДЛЯ XP =======================================================================================
            elif cmd == "fish_add_xp":
                print("Введите ID пользователя:")
                user_id = input().strip()

                if not user_id:
                    print("❌ Ошибка: ID пользователя не может быть пустым")
                    continue

                print("Введите количество XP для добавления:")

                amount = int(input().strip())
                user_xp = load_xp_data()
                if user_id not in user_xp:
                    user_xp[user_id] = 0
                    save_xp_data(user_xp)

                old_amount = user_xp[user_id]
                user_xp[user_id] += amount
                save_xp_data(user_xp)
                # level = calculate_level(current_xp)
                print(f"✅ Добавлено {amount} XP пользователю {user_id}")
                print(f"   Было: {old_amount} XP → Стало: {user_xp[user_id]} XP")
                print(f"   Было: {calculate_level(old_amount)}lvl → Стало: {calculate_level(user_xp[user_id])} lvl")

            elif cmd == "fish_check_xp":
                print("Введите ID пользователя для проверки XP:")
                user_id = input().strip()

                if not user_id:
                    print("❌ Ошибка: ID пользователя не может быть пустым")
                    continue

                user_xp = load_xp_data()
                xp = user_xp.get(user_id, 0)
                print(f"⭐ XP пользователя {user_id}: {xp}XP {calculate_level(user_xp[user_id])}lvl")



            elif cmd.strip() == "":
                continue  # Игнорируем пустые строки
            else:
                print(f"❓ Неизвестная команда: {cmd}")
                print("Введите 'fish_help' для списка команд")

        except EOFError:
            # Обработка Ctrl+C или закрытия терминала
            break
        except Exception as e:
            print(f"❌ Ошибка при выполнении команды: {e}")


# Запускаем проверку ввода в отдельном потоке
input_thread = threading.Thread(target=check_input, daemon=True)
input_thread.start()

print("Бот запущен. Введите 'fish_stop' в терминале для остановки")

try:
    while True:
        try:
            bot.polling(none_stop=True, timeout=5)
        except Exception as e:
            print(f"Ошибка: {e}")
            time.sleep(15)

except KeyboardInterrupt:
    print("Остановка по Ctrl+C")
