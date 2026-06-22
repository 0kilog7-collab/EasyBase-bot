import telebot
import requests
import json
import time
import os
from datetime import datetime, timedelta
from telebot import types

BOT_TOKEN = os.environ.get("BOT_TOKEN") or "8895180502:AAFHCyr_O7xp7-H0ZlpNjscM6Y1wxuQn4sw"
API_KEY = "DiC9ALodH5T12BfR"
SNUSBASE_KEY = "sb5029dec66mht55m78fx8bsw6tm8a"
bot = telebot.TeleBot(BOT_TOKEN)

REQUIRED_CHANNEL = -1004439932419
REQUIRED_CHANNEL_LINK = "https://t.me/Easyapl"

user_data = {}
user_requests = {}
user_bonus = {}

MAIN_TEXT = """
💡 Это бот для поиска информации по базам данных

🔍 Доступные типы поиска:
• Компании (по названию)
• Индивидуальные предприниматели (по ФИО)
• Физические лица (по ИНН)
• ИП (по ОГРН)
• Email (поиск в утечках)

📊 Лимиты:
• 5 запросов в день (основные)
• 3 бонусных запроса (активируются по кнопке)

📢 Канал: @Easyapl

Выберите действие:
"""

def check_subscription(user_id):
    try:
        member = bot.get_chat_member(REQUIRED_CHANNEL, user_id)
        return member.status in ['member', 'creator', 'administrator']
    except:
        return False

def escape_html(text):
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def get_user_today(user_id):
    today = datetime.now().strftime("%Y-%m-%d")
    if user_id not in user_requests:
        user_requests[user_id] = {"date": today, "count": 0}
    if user_requests[user_id]["date"] != today:
        user_requests[user_id] = {"date": today, "count": 0}
    return user_requests[user_id]

def get_user_bonus(user_id):
    if user_id not in user_bonus:
        user_bonus[user_id] = {"used": False}
    return user_bonus[user_id]

def can_make_request(user_id):
    if not check_subscription(user_id):
        return False, "Необходимо подписаться на канал"
    today_data = get_user_today(user_id)
    if today_data["count"] < 5:
        return True, f"Осталось {5 - today_data['count']} из 5"
    bonus_data = get_user_bonus(user_id)
    if not bonus_data["used"]:
        return True, "Бонусный запрос (1 из 3)"
    return False, "Лимит исчерпан. Завтра будет новый день."

def use_request(user_id):
    if not check_subscription(user_id):
        return False, "Подписка не найдена"
    today_data = get_user_today(user_id)
    if today_data["count"] < 5:
        today_data["count"] += 1
        return True, "Основной"
    bonus_data = get_user_bonus(user_id)
    if not bonus_data["used"]:
        bonus_data["used"] = True
        return True, "Бонусный"
    return False, None

def get_remaining(user_id):
    today_data = get_user_today(user_id)
    main_left = 5 - today_data["count"]
    bonus_data = get_user_bonus(user_id)
    bonus_left = 0 if bonus_data["used"] else 3
    return main_left, bonus_left

def format_response(data, query, search_type):
    response = f"🔍Найденные записи о {search_type}:\n┏<code>{escape_html(query)}</code>\n┃\n"
    
    if isinstance(data, list):
        for item in data:
            for key, value in item.items():
                if value and key not in ['Учред', 'Руковод']:
                    if isinstance(value, (dict, list)):
                        value = json.dumps(value, ensure_ascii=False)
                    response += f"┣{key}: <code>{escape_html(value)}</code>\n"
            response += "┃\n"
    elif isinstance(data, dict):
        for key, value in data.items():
            if value and key not in ['data', 'meta', 'Учред', 'Руковод']:
                if isinstance(value, (dict, list)):
                    value = json.dumps(value, ensure_ascii=False)
                response += f"┣{key}: <code>{escape_html(value)}</code>\n"
    
    response += "┗by: @xss_com"
    return response

def paginate_text(text, page=0, max_length=1500):
    if len(text) <= max_length:
        return text, None
    
    chunks = []
    current_chunk = ""
    
    for line in text.split('\n'):
        if len(current_chunk) + len(line) + 1 > max_length and current_chunk:
            chunks.append(current_chunk)
            current_chunk = line + '\n'
        else:
            current_chunk += line + '\n'
    
    if current_chunk:
        chunks.append(current_chunk)
    
    total_pages = len(chunks)
    page = max(0, min(page, total_pages-1))
    
    paginated_text = chunks[page]
    markup = None
    
    if total_pages > 1:
        markup = types.InlineKeyboardMarkup()
        btn_prev = types.InlineKeyboardButton("⬅️Назад", callback_data=f"page_{page-1}")
        btn_page = types.InlineKeyboardButton(f"{page+1}/{total_pages}", callback_data="current_page")
        btn_next = types.InlineKeyboardButton("➡️Вперёд", callback_data=f"page_{page+1}")
        markup.row(btn_prev, btn_page, btn_next)
    
    return paginated_text, markup

def show_main_menu(chat_id):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Поиск по компаниям", callback_data="search_company")
    btn2 = types.InlineKeyboardButton("Поиск по ФИО ИП", callback_data="search_entrepreneur")
    btn3 = types.InlineKeyboardButton("Поиск по ИНН Физ.", callback_data="search_inn")
    btn4 = types.InlineKeyboardButton("Поиск по ОГРН ИП", callback_data="search_ogrn")
    btn5 = types.InlineKeyboardButton("Поиск по email (утечки)", callback_data="search_email")
    btn6 = types.InlineKeyboardButton("Бонусные запросы (3 шт)", callback_data="get_bonus")
    btn7 = types.InlineKeyboardButton("Статистика", callback_data="show_stats")
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    markup.row(btn5)
    markup.row(btn6, btn7)
    bot.send_message(chat_id, MAIN_TEXT, parse_mode='HTML', reply_markup=markup)

# ===== ВСЕ ХЕНДЛЕРЫ (те же, что у тебя) =====
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if check_subscription(user_id):
        show_main_menu(message.chat.id)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Подписаться на канал", url=REQUIRED_CHANNEL_LINK))
        markup.add(types.InlineKeyboardButton("✅ Я подписался", callback_data="check_sub"))
        bot.send_message(message.chat.id, "📢 Подпишитесь на наш канал:\n\n" + REQUIRED_CHANNEL_LINK, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_sub_callback(call):
    user_id = call.from_user.id
    if check_subscription(user_id):
        bot.answer_callback_query(call.id, "✅ Подписка подтверждена!")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_main_menu(call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, "❌ Вы не подписались!", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "get_bonus")
def handle_bonus(call):
    user_id = call.from_user.id
    if not check_subscription(user_id):
        bot.answer_callback_query(call.id, "❌ Подпишитесь на канал!", show_alert=True)
        return
    bonus_data = get_user_bonus(user_id)
    if bonus_data["used"]:
        bot.answer_callback_query(call.id, "❌ Бонус уже использован!")
        return
    bonus_data["used"] = True
    bot.answer_callback_query(call.id, "✅ Бонус активирован!")
    bot.send_message(call.message.chat.id, "🎁 +3 бонусных запроса активированы!")

@bot.callback_query_handler(func=lambda call: call.data == "show_stats")
def show_stats(call):
    user_id = call.from_user.id
    if not check_subscription(user_id):
        bot.answer_callback_query(call.id, "❌ Подпишитесь на канал!", show_alert=True)
        return
    main_left, bonus_left = get_remaining(user_id)
    text = f"📊 Статистика:\n\n🔹 Основные: {main_left}/5\n🎁 Бонусные: {bonus_left}/3\n📌 Всего: {main_left + bonus_left}"
    bot.send_message(call.message.chat.id, text)

@bot.callback_query_handler(func=lambda call: call.data.startswith('page_'))
def handle_pagination(call):
    user_id = call.from_user.id
    if user_id not in user_data:
        return bot.answer_callback_query(call.id, "Данные устарели")
    new_page = int(call.data.split('_')[1])
    search_data = user_data[user_id]
    formatted_text = format_response(json.loads(search_data['text']), search_data['query'], search_data['type'])
    paginated_text, markup = paginate_text(formatted_text, new_page)
    try:
        bot.edit_message_text(paginated_text, call.message.chat.id, call.message.message_id, parse_mode='HTML', reply_markup=markup)
        bot.answer_callback_query(call.id)
    except:
        bot.answer_callback_query(call.id, "Ошибка")

@bot.callback_query_handler(func=lambda call: call.data == "current_page")
def handle_current_page(call):
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('search_'))
def handle_search(call):
    user_id = call.from_user.id
    if not check_subscription(user_id):
        bot.answer_callback_query(call.id, "❌ Подпишитесь на канал!", show_alert=True)
        return
    can, msg = can_make_request(user_id)
    if not can:
        bot.answer_callback_query(call.id, f"❌ {msg}", show_alert=True)
        return
    search_type = call.data.split('_')[1]
    search_types = {
        'company': "Введите название компании:",
        'entrepreneur': "Введите ФИО ИП:",
        'inn': "Введите ИНН физического лица:",
        'ogrn': "Введите ОГРН ИП:",
        'email': "Введите email для проверки в утечках:"
    }
    msg = bot.send_message(call.message.chat.id, search_types[search_type])
    bot.register_next_step_handler(msg, lambda m: process_search(m, search_type))

def process_search(message, search_type):
    user_id = message.from_user.id
    if not check_subscription(user_id):
        bot.send_message(message.chat.id, "❌ Подпишитесь на канал!")
        return
    can, msg = can_make_request(user_id)
    if not can:
        bot.send_message(message.chat.id, f"❌ {msg}")
        return
    query = message.text.strip()
    urls = {
        'company': f"https://api.ofdata.ru/v2/search?key={API_KEY}&by=name&obj=org&query={query}",
        'entrepreneur': f"https://api.ofdata.ru/v2/search?key={API_KEY}&by=founder-name&obj=org&query={query}",
        'inn': f"https://api.ofdata.ru/v2/person?key={API_KEY}&inn={query}",
        'ogrn': f"https://api.ofdata.ru/v2/inspections?key={API_KEY}&ogrn={query}"
    }
    request_type, request_label = use_request(user_id)
    if not request_type:
        bot.send_message(message.chat.id, "❌ Лимит исчерпан")
        return
    if search_type == 'email':
        try:
            headers = {"Content-Type": "application/json", "Auth": SNUSBASE_KEY}
            payload = {"terms": [query], "types": ["email"], "wildcard": False}
            response = requests.post("https://api.snusbase.com/data/search", headers=headers, json=payload, timeout=10)
            data = response.json()
            if data.get('size', 0) > 0:
                records = []
                for db, results in data.get('results', {}).items():
                    for row in results:
                        records.append(row)
                if records:
                    user_data[message.from_user.id] = {
                        'text': json.dumps(records, ensure_ascii=False),
                        'type': "email (утечки)",
                        'query': query
                    }
                    formatted_text = format_response(records, query, "email")
                    paginated_text, markup = paginate_text(formatted_text)
                    bot.send_message(message.chat.id, f"✅ {request_label} запрос использован")
                    bot.send_message(message.chat.id, paginated_text, parse_mode='HTML', reply_markup=markup)
                    return
            bot.send_message(message.chat.id, f"❌ Данные не найдены ({request_label} запрос использован)")
        except:
            bot.send_message(message.chat.id, "❌ Ошибка запроса")
        return
    try:
        response = requests.get(urls[search_type], timeout=5)
        data = response.json()
        if data.get('meta', {}).get('status') == 'ok':
            records = data.get('data', {}).get('Записи', data.get('data', {}))
            if records:
                user_data[message.from_user.id] = {
                    'text': json.dumps(records, ensure_ascii=False),
                    'type': {
                        'company': "компании",
                        'entrepreneur': "ФИО ИП",
                        'inn': "ИНН Физ",
                        'ogrn': "ОГРН ИП"
                    }[search_type],
                    'query': query
                }
                formatted_text = format_response(records, query, user_data[message.from_user.id]['type'])
                paginated_text, markup = paginate_text(formatted_text)
                bot.send_message(message.chat.id, f"✅ {request_label} запрос использован")
                bot.send_message(message.chat.id, paginated_text, parse_mode='HTML', reply_markup=markup)
                return
        bot.send_message(message.chat.id, f"❌ Данные не найдены ({request_label} запрос использован)")
    except:
        bot.send_message(message.chat.id, "❌ Ошибка запроса")

# ===== ЗАПУСК ДЛЯ RENDER =====
if __name__ == "__main__":
    print("Bot started!")
    bot.infinity_polling()
