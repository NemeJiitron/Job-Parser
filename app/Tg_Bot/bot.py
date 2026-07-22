from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Application, CommandHandler, ContextTypes, CallbackContext, ConversationHandler,
                          CallbackQueryHandler, MessageHandler, filters)
import os
from dotenv import load_dotenv
from app.database import Session_local
from app.router.jobs import get_parser, fetch_offers_by, delete_by

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Search for offers", callback_data="search_offers")],
        [InlineKeyboardButton("Delete offers", callback_data="delete_offers")],
        [InlineKeyboardButton("Get offers", callback_data="get_offers")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_text("Main menu.", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text("Main menu.", reply_markup=reply_markup)
    return 'menu'

async def jobs(update: Update, context: CallbackContext):
    q = update.callback_query
    if q.data == 'menu_back':
        return await start(update, context)
    elif q.data == 'delete_offers':
        context.user_data['mode'] = 'delete'
        keyboard = [
            [InlineKeyboardButton("Clear all", callback_data="clear")],
            [InlineKeyboardButton("Delete by filter", callback_data="delete_by")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await q.edit_message_text("Deletion menu.", reply_markup=reply_markup)
        return 'delete'
    if q.data == 'search_offers':
        context.user_data['mode'] = 'search'
    elif q.data == 'get_offers':
        context.user_data['mode'] = 'fetch'
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Profesia.sk", callback_data="profesia")]])
    await q.edit_message_text("Сhoose source:", reply_markup=reply_markup)
    return 'source'

async def delete(update: Update, context: CallbackContext):
    q = update.callback_query
    await q.answer()
    if q.data == 'clear':
        db = Session_local()
        try:
            delete_by(db, telegram_id=str(update.effective_user.id))
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Back to Menu", callback_data="menu_back")]])
            await q.edit_message_text(f"Deletion completed.", reply_markup=reply_markup)
            return 'menu'
        finally:
            db.close()
    else:
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Profesia.sk", callback_data="profesia")]])
        await q.edit_message_text("Сhoose source:", reply_markup=reply_markup)
        return 'source'
async def choose_source(update: Update, context: CallbackContext):
    q = update.callback_query
    await q.answer()
    context.user_data['source'] = q.data
    await q.edit_message_text("Choose location:")
    return "location"

async def enter_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['location'] = update.message.text
    await update.message.reply_text("Enter keyword (type \"-\" to skip):")
    return "keyword"

async def enter_keyword(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['keyword'] = update.message.text if update.message.text != '-' else None
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Back to Menu", callback_data="menu_back")]])
    await update.message.reply_text("Hold on, we're processing your query...")
    db = Session_local()
    try:
        if context.user_data['mode'] == 'fetch':
            offers = fetch_offers_by(db, context.user_data['location'], context.user_data['source'], context.user_data['keyword'], telegram_id=str(update.effective_user.id))
            text = ""
            for offer in offers:
                text += f"Title: {offer.title}\nCompany:{offer.company}\nURL: {offer.url}\n{'-' * 10}\n"
            if text != "":
                await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)
            else:
                await update.message.reply_text("No offers found!", reply_markup=reply_markup)
        elif context.user_data['mode'] == 'search':
            parser = get_parser(context.user_data['source'])
            added = parser.parse(db, context.user_data['location'], context.user_data['keyword'], tg_id=str(update.effective_user.id))
            await update.message.reply_text(f"Added {added} offers", reply_markup=reply_markup)
        elif context.user_data['mode'] == 'delete':
            delete_by(db, context.user_data['location'], context.user_data['source'], context.user_data['keyword'], telegram_id=str(update.effective_user.id))
            await update.message.reply_text(f"Deletion completed.", reply_markup=reply_markup)
    except:
        raise Exception("Input is invalid")
    finally:
        db.close()
    context.user_data['mode'] = None
    return 'menu'

conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        "menu": [CallbackQueryHandler(jobs)],
        "delete": [CallbackQueryHandler(delete)],
        "source": [CallbackQueryHandler(choose_source)],
        "location": [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_location)],
        "keyword": [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_keyword)],
    },
    fallbacks=[]
)


def run_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(conversation_handler)
    app.run_polling()

if __name__ == "__main__":
    run_bot()