from telegram import *
from telegram.ext import *
import logging
from menus import *
from bot_token import bot_token
from db_bot import *


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------

# conversation states
ROUTE, DEPART, DIRECTION, SCHEDULE = range(4)


# ask route
def route(bot, update):
    update.message.reply_text(
        'Расписание автобусов города Видное.\n'
        'Номер маршрута?',
        reply_markup=ReplyKeyboardMarkup(route_menu(), resize_keyboard=True, one_time_keyboard=True))
    return ROUTE


# ask the stop to depart
def depart(bot, update):
    update.message.reply_text(
        'От какой остановки?',
        reply_markup=ReplyKeyboardMarkup(depart_menu(), resize_keyboard=True, one_time_keyboard=True))
    return DEPART


# ask direction
def direction(bot, update):
    update.message.reply_text(
        'В какую сторону?',
        reply_markup=ReplyKeyboardMarkup(direction_menu(), resize_keyboard=True, one_time_keyboard=True))
    return DIRECTION


# navigate schedule
def schedule(bot, update):
    update.message.reply_text(
        '<здесь будет расписание>',
        reply_markup=ReplyKeyboardMarkup(schedule_menu(), resize_keyboard=True, one_time_keyboard=True))
    return SCHEDULE


# fallback
def cancel(bot, update):
    return ConversationHandler.END


# logging
def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


# -------------------------------------------------------------------------------------------------------

def main():
    updater = Updater(token=bot_token)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', route)],

        states={
            ROUTE: [
                RegexHandler(route_menu_re(), depart),
                RegexHandler(template_of([BACK_TO_START]), route)],

            DEPART: [
                RegexHandler(depart_menu_re(), direction),
                RegexHandler(template_of([BACK_TO_START]), route)],

            DIRECTION: [
                RegexHandler(direction_menu_re(), schedule),
                RegexHandler(template_of([BACK_TO_START]), route)],

            SCHEDULE: [
                RegexHandler(schedule_menu_re(), schedule),
                RegexHandler(template_of([BACK_TO_START]), route)]
        },

        fallbacks=[CommandHandler('start', route)]
    )

    dispatcher.add_handler(conv_handler)

    # log all errors
    dispatcher.add_error_handler(error)

    # go!
    print('Polling...')
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()