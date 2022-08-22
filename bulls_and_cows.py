from operator import index
import functions as f
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup
import telegram
import logging
import functions as f
from config import TOKEN

# #context.bot.send_sticker(update.effective_chat.id,
#                              'CAACAgIAAxkBAAIHB2L773CFUgSrJAJuSysSKC-13TffAAIeAAPANk8ToWBbLasAAd4EKQQ')
bulls = 0
cows = 0
secret_word = ''
user_word = ''
count = 0

bot = telegram.Bot(TOKEN)

updater = Updater(
    token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

GAME, YESNO = range(2)


def start(update, context):
    task = str('Добро пожаловать в игру "Быки и коровы"! Сейчас расскажу тебе правила!'
               'Загадано слово и тебе нужно его угадать. Колличество попыток - это колличество букв'
               "Если буквы на своём месте - это быки, если нет - это коровы"
               "После каждого хода будет уведомление о колличестве быков и коров")
    context.bot.send_sticker(update.effective_chat.id,
                             'CAACAgIAAxkBAAEFpaljBAS4V96UItT2WGSz-Pafe5AGugAC4AgAAi8P8AYAAXaEuQTrqIApBA')
    context.bot.send_message(chat_id=update.effective_chat.id, text=task)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text='Играем? да/нет')
    return YESNO


def yesno(update, context):
    global secret_word, bulls, cows, count, user_word
    secret_word = f.for_bulls_and_cows()
    word = list(secret_word)
    print(word)

    if str(update.message.text).lower() == 'да':

        context.bot.send_sticker(update.effective_chat.id,
                                 'CAACAgIAAxkBAAEFpatjBAVOE2QElxM-MrGRcty91aTTbQACyAADLw_wBgmOfoErjolZKQQ')
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f'Я загадал слово из {len(word)} букв. Введи своё слово')
        return GAME

    if str(update.message.text).lower() == 'нет':
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="ОК. До встречи! Поиграем в следующий раз!")
        context.bot.send_sticker(
            update.effective_chat.id, 'CAACAgIAAxkBAAEFpa1jBAWHsIZkvtnllBBbPmASYWLP0gAC2AADLw_wBoDX6pSyEYj-KQQ')
        return ConversationHandler.END
    else:
        context.bot.send_sticker(update.effective_chat.id,
                                 'CAACAgIAAxkBAAEFpa9jBAWwJXG7t0ynDnrDv0tcCWo3NQACsgADLw_wBlD8ocbVBWp8KQQ')
        context.bot.send_message(
            chat_id=update.effective_chat.id, text='Я тебя не понимаю. Напиши "да" или "нет"')
        return YESNO


def game(update, context):
    global secret_word, bulls, cows, count, user_word
    word = list(secret_word)
    user_word = list(str(update.message.text))
    if len(user_word) != len(word):
        context.bot.send_sticker(update.effective_chat.id,
                                 'CAACAgIAAxkBAAEFpbVjBAcja4_WTZb2VrmOKvlRIMyRDQAC0gADLw_wBnr0oooxhszbKQQ')
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=f'Введи слово из {len(word)} букв')
        return GAME
    else:
        for i in word:
            if i in user_word:
                if user_word.index(i) == word.index(i):
                    bulls += 1
                else:
                    cows += 1
        count += 1
        if bulls == len(word):
            context.bot.send_sticker(update.effective_chat.id,
                                     'CAACAgIAAxkBAAEFpbFjBAXKVTr9ED8JsrBstoHkr3vN9wACrAADLw_wBl3CdytzaH_QKQQ')
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=f'Поздравляю! Ты победил!')
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=f'Поиграем ещё? да/нет')
            bulls = 0
            cows = 0
            count = 0
            return YESNO
        elif count == len(word):
            context.bot.send_sticker(update.effective_chat.id,
                                     'CAACAgIAAxkBAAEFpbNjBAX4xVDXTUCLwut2CySM52HifgAC0AADLw_wBtZYso6UcDn1KQQ')
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=f'Ты проиграл!')
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=f'Поиграем ещё? да/нет')
            count = 0
            bulls = 0
            cows = 0
            return YESNO
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f'Быков {bulls}, коров {cows}. Осталось {len(word)-count} попыток.')
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=f'Попробуй ещё раз!')
            bulls = 0
            cows = 0


def end(update, context):
    user = update.message.from_user  # определяем пользователя
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Конец игры!")
    # Заканчиваем игру. Не работает.
    return ConversationHandler.END


candy_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        YESNO: [MessageHandler(Filters.text, yesno)],
        GAME: [MessageHandler(Filters.text, game)]
    },
    fallbacks=[CommandHandler('end', end)],
)


dispatcher.add_handler(candy_handler)


print('start bot')
updater.start_polling()
updater.idle()
