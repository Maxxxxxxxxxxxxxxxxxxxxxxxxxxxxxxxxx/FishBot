from telebot import util
import telebot
import os
import json
import random
import time
import threading
from secrets import secrets
from telebot import types
from fish_list import *
from logic_json import *
import rods_f
import bait_f
import boat_f
from telebot import apihelper



# Глобальные переменные
last_message_id = None
user_cooldowns = {}
user_bets = {}
user_xp = load_xp_data()
selected_bait = bait_f.load_bait_select()
inline_sessions = {}

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


def menu_button(chat_id, inline_message_id=None):
    global last_message_id

    user_id = str(chat_id)
    user_bait_data = load_bait_data()
    markup = types.InlineKeyboardMarkup(row_width=2)

    btn1 = types.InlineKeyboardButton("Shop", callback_data='button_shop')
    btn2 = types.InlineKeyboardButton("Fishing", callback_data='sub_button_menu')
    btn3 = types.InlineKeyboardButton("Coinflip", callback_data='coinflip_menu')
    markup.add(btn2, btn1, btn3)

    selected_bait = bait_f.load_bait_select()
    user_money = load_money_data()

    text = f"""Menu:
Balance: {user_money.get(user_id, 0)}$
XP: {user_xp.get(user_id, 0)}
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
        user_xp[user_id] += xp_price1()
        save_xp_data(user_xp)

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
    elif call.data == 'bait':
        bait_f.bait_func(call.from_user.id, inline_msg_id if inline_msg_id else call.message.message_id)
    elif call.data == 'Worms':
        if selected_bait[user_id] in ["Worms"]:
            bait_f.save_state_bait(selected_bait)
            bait_f.callback_query_bait(call)
            user_bait_data = load_bait_data()
            user_bait_data[user_id]["Worms"] += 20
            save_bait_data(user_bait_data)
            return

        if user_money[user_id] >= 80:
            user_money[user_id] -= 80
            save_money_data(user_money)
            bait_type = "Worms"
            selected_bait[user_id] = bait_f.load_bait_select()
            user_bait_data = load_bait_data()
            if (bait_type not in selected_bait[user_id]) and (user_bait_data[user_id]["Worms"] > 0):
                selected_bait[user_id] = "Empty"
                bait_f.save_state_bait(selected_bait)
                bait_f.callback_query_bait(call)
            else:
                selected_bait[user_id] = "Worms"
                bait_f.save_state_bait(selected_bait)
                bait_f.callback_query_bait(call)
                user_bait_data[user_id][bait_type] = 20
                save_bait_data(user_bait_data)
            save_bait_data(user_bait_data)
        elif user_bait_data[user_id]["Worms"] > 0:
            bait_f.callback_query_bait(call)
        else:
            bot.answer_callback_query(call.id, text="You don't have enough money(", show_alert=False)
    elif call.data == 'Leeches':
        if selected_bait[user_id] in ["Leeches"]:
            bait_f.save_state_bait(selected_bait)
            bait_f.callback_query_bait(call)
            user_bait_data = load_bait_data()
            user_bait_data[user_id]["Leeches"] += 20
            save_bait_data(user_bait_data)
            return

        if user_money[user_id] >= 80:
            user_money[user_id] -= 80
            save_money_data(user_money)
            bait_type = "Leeches"
            selected_bait[user_id] = bait_f.load_bait_select()
            user_bait_data = load_bait_data()
            if (bait_type not in selected_bait[user_id]) and (user_bait_data[user_id]["Leeches"] > 0):
                selected_bait[user_id] = "Empty"
                bait_f.save_state_bait(selected_bait)
                bait_f.callback_query_bait(call)
            else:
                selected_bait[user_id] = "Leeches"
                bait_f.save_state_bait(selected_bait)
                bait_f.callback_query_bait(call)
                user_bait_data[user_id][bait_type] = 20
                save_bait_data(user_bait_data)
            save_bait_data(user_bait_data)
        elif user_bait_data[user_id]["Leeches"] > 0:
            bait_f.callback_query_bait(call)
        else:
            bot.answer_callback_query(call.id, text="You don't have enough money(", show_alert=False)
    elif call.data == 'Magnet':
        if selected_bait[user_id] in ["Magnet"]:
            bait_f.save_state_bait(selected_bait)
            bait_f.callback_query_bait(call)
            user_bait_data = load_bait_data()
            user_bait_data[user_id]["Magnet"] += 20
            save_bait_data(user_bait_data)
            return

        if user_money[user_id] >= 80:
            user_money[user_id] -= 80
            save_money_data(user_money)
            bait_type = "Magnet"
            selected_bait[user_id] = bait_f.load_bait_select()
            user_bait_data = load_bait_data()
            if (bait_type not in selected_bait[user_id]) and (user_bait_data[user_id]["Magnet"] > 0):
                selected_bait[user_id] = "Empty"
                bait_f.save_state_bait(selected_bait)
                bait_f.callback_query_bait(call)
            else:
                selected_bait[user_id] = "Magnet"
                bait_f.save_state_bait(selected_bait)
                bait_f.callback_query_bait(call)
                user_bait_data[user_id][bait_type] = 20
                save_bait_data(user_bait_data)
            save_bait_data(user_bait_data)
        elif user_bait_data[user_id]["Magnet"] > 0:
            bait_f.callback_query_bait(call)
        else:
            bot.answer_callback_query(call.id, text="You don't have enough money(", show_alert=False)

    bot.answer_callback_query(call.id)


def fish_menu(call):
    global last_message_id

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
    fMAX = (rod_number ** 2) + (bait_number * 8) + random.choice([-1, -2, 1, 2, 3, 4, 5, 6, 3, 2, 3]) + (
                boat_number * 20)

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
            if random.randint(1, 5) == 2:
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
            for _ in range(abs(fMAX - 8)):
                temp_fish = random.choice(temp_fishlist)
                parts = temp_fish.split()
                temp_money += int(parts[0])
                temp_xp += int(parts[1])
                fish_list.append(parts[2])
            if random.randint(1, 10) <= 3:
                CHparts = ChestT2.split()
                temp_money += int(CHparts[0])
                temp_xp += int(CHparts[1])
                fish_list.append(CHparts[2])
            elif random.randint(1, 10) == 10:
                CHparts = ChestT3.split()
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

    elif current_rod in ['rod4']:
        temp_fishlist = random.choice(T3)
        if isinstance(temp_fishlist, tuple):
            for _ in range(abs(fMAX - 5)):
                temp_fish = random.choice(temp_fishlist)
                parts = temp_fish.split()
                temp_money += int(parts[0])
                temp_xp += int(parts[1])
                fish_list.append(parts[2])
            if random.randint(1, 10) <= 3:
                CHparts = ChestT3.split()
                temp_money += int(CHparts[0])
                temp_xp += int(CHparts[1])
                fish_list.append(CHparts[2])
            elif random.randint(1, 10) == 10:
                CHparts = ChestT4.split()
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

    elif current_rod in ['rod5']:
        temp_fishlist = random.choice(T4)
        if isinstance(temp_fishlist, tuple):
            for _ in range(abs(fMAX - 5)):
                temp_fish = random.choice(temp_fishlist)
                parts = temp_fish.split()
                temp_money += int(parts[0])
                temp_xp += int(parts[1])
                fish_list.append(parts[2])
            if random.randint(1, 10) <= 3:
                CHparts = ChestT4.split()
                temp_money += int(CHparts[0])
                temp_xp += int(CHparts[1])
                fish_list.append(CHparts[2])
            elif random.randint(1, 10) == 10:
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

    elif current_rod in ['rod6', 'rod7', 'rod8']:
        for _ in range(fMAX):
            temp_fish = random.choice(LavaT1)
            for temp_fish in temp_fish:
                parts = temp_fish.split()
                temp_money += int(parts[0])
                temp_xp += int(parts[1])
                fish_list.append(parts[2])
            if random.randint(1, 10) <= 3:
                CHparts = ChestT4.split()
                temp_money += int(CHparts[0])
                temp_xp += int(CHparts[1])
                fish_list.append(CHparts[2])
            elif random.randint(1, 15) == 9:
                CHparts = ChestT5.split()
                temp_money += int(CHparts[0])
                temp_xp += int(CHparts[1])
                fish_list.append(CHparts[2])
            elif random.randint(1, 15) == 10:
                CHparts = ChestT3.split()
                temp_money += int(CHparts[0])
                temp_xp += int(CHparts[1])
                fish_list.append(CHparts[2])
            fish_list = sorted(fish_list)

    fish_counts = {fish: fish_list.count(fish) for fish in set(fish_list)}
    message_text = f"{call.from_user.first_name}\n\nYou caught:\n"
    for fish, count in fish_counts.items():
        message_text += f"x{count} {fish}\n"
    message_text += f"\n +{temp_money}$\n +{temp_xp} XP"

    user_money = load_money_data()
    user_money[user_id] += temp_money
    save_money_data(user_money)

    user_xp[user_id] += temp_xp
    save_xp_data(user_xp)

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
        types.InlineKeyboardButton("fish again", callback_data='sub_btn_fish'),
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




while True:
    try:
        bot.polling(none_stop=True)

    except Exception as e:
        print(e)

        time.sleep(15)