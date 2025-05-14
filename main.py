import logging
import os
from telegram import __version__ as TG_VER
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# Проверка версии библиотеки python-telegram-bot
try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)
if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(f"Требуется python-telegram-bot 20.0+. Текущая версия: {TG_VER}")

# Получение токена из переменной окружения
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
if not TELEGRAM_TOKEN:
    raise ValueError("Telegram token не найден! Установите переменную TELEGRAM_TOKEN")

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Категории товаров
CATEGORIES = [
    {
        "emoji": "💻",
        "name": "Ноутбуки и планшеты",
        "description": "Ноутбуки, планшеты, 2-в-1 устройства от ведущих брендов",
        "url": "https://osait.ru/category/noutbuki-i-planshety/ "
    },
    {
        "emoji": "🖥️",
        "name": "Компьютеры",
        "description": "Системные блоки, моноблоки и серверные решения",
        "url": "https://osait.ru/category/kompyutery/ "
    },
    {
        "emoji": "📱",
        "name": "Мобильная связь",
        "description": "Смартфоны, смарт-часы и аксессуары",
        "url": "https://osait.ru/category/mobilnaya-svyaz/ "
    },
    {
        "emoji": "📺",
        "name": "Телевизоры и аксессуары",
        "description": "LED/Smart TV, крепления и медиаплееры",
        "url": "https://osait.ru/category/televizory-i-aksessuary/ "
    },
    {
        "emoji": "🖱️",
        "name": "Комплектующие для компьютеров",
        "description": "Процессоры, видеокарты, SSD и охлаждение",
        "url": "https://osait.ru/category/komplektuyushchie-dlya-kompyuterov/ "
    },
    {
        "emoji": "🎮",
        "name": "Оборудование для геймеров",
        "description": "Игровые консоли, геймпады и гарнитуры",
        "url": "https://osait.ru/category/oborudovanie-dlya-geymerov/ "
    },
    {
        "emoji": "🖨️",
        "name": "Периферия и аксессуары",
        "description": "Клавиатуры, мыши, колонки и веб-камеры",
        "url": "https://osait.ru/category/periferiya-i-aksessuary/ "
    },
    {
        "emoji": "🏠",
        "name": "Бытовая техника для дома",
        "description": "Холодильники, стиральные машины и климатическая техника",
        "url": "https://osait.ru/category/bytovaya-tekhnika-dlya-doma/ "
    },
    {
        "emoji": "🎧",
        "name": "Аудио-видео техника",
        "description": "Hi-Fi системы, наушники и проекторы",
        "url": "https://osait.ru/category/audio-video-tekhnika/ "
    },
    {
        "emoji": "⚡",
        "name": "Портативная электроника",
        "description": "Powerbank'и, портативные колонки и электронные книги",
        "url": "https://osait.ru/category/portativnaya-elektronika/ "
    },
    {
        "emoji": "🗄️",
        "name": "Серверы и СХД",
        "description": "Серверные шасси, NAS и системы хранения данных",
        "url": "https://osait.ru/category/servery-i-skhd/ "
    },
    {
        "emoji": "🌐",
        "name": "Сетевое оборудование",
        "description": "Роутеры, маршрутизаторы и сетевые карты",
        "url": "https://osait.ru/category/setevoe-oborudovanie/ "
    },
    {
        "emoji": "💿",
        "name": "Программное обеспечение",
        "description": "Операционные системы, антивирусы и профессиональный софт",
        "url": "https://osait.ru/category/programmnoe-obespechenie/ "
    }
]

# Клавиатуры
MAIN_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("🚀 Каталог", callback_data="catalog")],
    [InlineKeyboardButton("ℹ️ О нас", callback_data="about")],
    [InlineKeyboardButton("📞 Контакты", callback_data="contacts")],
    [InlineKeyboardButton("❓ Помощь", callback_data="help")]
])
BACK_TO_MAIN_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("◀️ Назад в меню", callback_data="back_to_main")]
])
CATALOG_BACK_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("◀️ Назад к категориям", callback_data="catalog")]
])

# Обработчики команд и кнопок
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.edit_text(
            "Привет! 🤖 Я помощник OSAIT\n"
            "Чем могу помочь?\n"
            "👉 Выберите категорию\n"
            "👉 Узнайте о нас\n"
            "👉 Свяжитесь с поддержкой",
            reply_markup=MAIN_KEYBOARD
        )
    else:
        await update.message.reply_text(
            "Привет! 🤖 Я помощник OSAIT\n"
            "Чем могу помочь?\n"
            "👉 Выберите категорию\n"
            "👉 Узнайте о нас\n"
            "👉 Свяжитесь с поддержкой",
            reply_markup=MAIN_KEYBOARD
        )

async def catalog(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    keyboard = []
    for idx, category in enumerate(CATEGORIES):
        keyboard.append([
            InlineKeyboardButton(
                f"{category['emoji']} {category['name']}",
                callback_data=f"cat_{idx}"
            )
        ])
    keyboard.append([InlineKeyboardButton("◀️ Назад в меню", callback_data="back_to_main")])
    await query.message.edit_text(
        "Каталог товаров:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    category_idx = int(query.data.split("_")[1])
    category = CATEGORIES[category_idx]
    keyboard = [
        [InlineKeyboardButton("🌐 Перейти на сайт", url=category['url'])],
        [InlineKeyboardButton("◀️ Назад к категориям", callback_data="catalog")]
    ]
    await query.message.edit_text(
        f"{category['emoji']} *{category['name']}*\n"
        f"{category['description']}",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.message.edit_text(
        "О компании OSAIT:\n"
        "Мы - ведущий поставщик цифровой техники в России\n"
        "Основаны в 2020 году\n"
        "Более 100 тыс. довольных клиентов\n"
        "Собственный сервисный центр",
        reply_markup=BACK_TO_MAIN_KEYBOARD
    )

async def contacts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("WhatsApp", url="https://wa.me/79823143855 ")],
        [InlineKeyboardButton("Telegram", url="https://t.me/osait_support ")],
        [InlineKeyboardButton("🗺️ Google Maps", url="https://goo.gl/maps/example ")],
        [InlineKeyboardButton("◀️ Назад в меню", callback_data="back_to_main")]
    ]
    await query.message.edit_text(
        "Контакты OSAIT:\n"
        "📧 ooo_osa@internet.ru\n"
        "📞 +7 (982) 314-38-55\n"
        "📍 Москва, ул. Примерная, 1",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("FAQ", url="https://osait.ru/faq ")],
        [InlineKeyboardButton("Чат-поддержка", url="https://t.me/osait_support ")],
        [InlineKeyboardButton("◀️ Назад в меню", callback_data="back_to_main")]
    ]
    await query.message.edit_text(
        "Помощь:\n"
        "/start - Главное меню\n"
        "/faq - Частые вопросы\n"
        "Поддержка: 24/7",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await start(update, context)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.lower()
    if any(word in text for word in ["привет", "здравствуй", "добрый день"]):
        await update.message.reply_text(
            "Привет! 😊 Рад вас видеть!\n"
            "Чем могу помочь сегодня?",
            reply_markup=MAIN_KEYBOARD
        )
    elif any(word in text for word in ["пока", "до свидания", "увидимся"]):
        await update.message.reply_text(
            "До встречи! 🌟\n"
            "Всегда рады помочь - возвращайтесь!"
        )
    else:
        await update.message.reply_text(
            "К сожалению, я не понимаю ваш запрос 🤔\n"
            "Используйте кнопки меню или напишите /start"
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.error(f"Произошла ошибка: {context.error}")
    if update:
        try:
            await update.message.reply_text(
                "Произошла непредвиденная ошибка 😢\n"
                "Попробуйте позже или свяжитесь с поддержкой"
            )
        except Exception as e:
            logging.error(f"Ошибка при отправке сообщения об ошибке: {e}")

def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(catalog, pattern="^catalog$"))
    application.add_handler(CallbackQueryHandler(about, pattern="^about$"))
    application.add_handler(CallbackQueryHandler(contacts, pattern="^contacts$"))
    application.add_handler(CallbackQueryHandler(help_command, pattern="^help$"))
    application.add_handler(CallbackQueryHandler(show_category, pattern="^cat_"))
    application.add_handler(CallbackQueryHandler(back_to_main, pattern="^back_to_main$"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    application.run_polling()

if __name__ == "__main__":
    main()
