
from asyncio.log import logger
import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup
import telegram
import logging
import functions as f
from config import TOKEN


START, USER, YESNO, BANK, LEVEL, CANDY = range(6)

logger = logging.getLogger('logger')
case_lever = logging.getLogger('case_lever')
bank_candys = None
max_candys_step = None
logger.info = bank_candys
user_name = ''


bot = telegram.Bot(TOKEN)

updater = Updater(
    token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


def game(update, context):

    task = str('Добро пожаловать в игру "Забери конфеты"! Сейчас расскажу тебе правила!'
               'На столе лежит кучка конфет. Играют два игрока делая ход друг после друга.'
               "За один ход можно забрать не более определённого колличества конфет."
               "Тот, кто берет последнюю конфету - выйграл. ")
    context.bot.send_sticker(update.effective_chat.id,
                             'CAACAgIAAxkBAAEFpadjBALmNpQp-eEyKIVQY8ulWlAZkwACmQwAAj9UAUrPkwx5a8EilCkE')           
    context.bot.send_message(chat_id=update.effective_chat.id, text=task)

    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Давай познакомимся! Как тебя зовут?")
    context.bot.send_sticker(update.effective_chat.id,
                             'CAACAgIAAxkBAAIHB2L773CFUgSrJAJuSysSKC-13TffAAIeAAPANk8ToWBbLasAAd4EKQQ')
    return USER


def get_name(update, context):
    global user_name
    user_name = str(update.message.text)

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"Рад знакомству, {user_name}! Ты готов(а) играть?: да/нет")
    return YESNO


def user_yes_no(update, context):
    global bank_candys

    if str(update.message.text).lower() == 'да':
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Отлично! Сколько конфет разыграем?")
        return BANK
    if str(update.message.text).lower() == 'нет':
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="ОК. До встречи! Поиграем в следующий раз!")
        context.bot.send_sticker(
            update.effective_chat.id, 'CAACAgIAAxkBAAIHCWL779dyo3XXRB7S6swbvZ2UVIu2AAIMAAMkcWIax6R7FEdriGIpBA')
        return ConversationHandler.END
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text='Я тебя не понимаю. Напиши "да" или "нет"')
        return YESNO


def get_candys(update, context):
    global bank_candys
    if update.message.text.isdigit() == False:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Нужно ввести число!")
    else:
        bank_candys = int(update.message.text)

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Класс! По сколько конфет можно брать за ход?")
        return LEVEL


def level(update, context):
    global max_candys_step
    if update.message.text.isdigit() == False:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Нужно ввести число!")
    else:
        max_candys_step = int(update.message.text)
    keyboard = [
        ['Простой(против бота)', 'Сложный(против бота с интеллектом ']]
    markup_key = ReplyKeyboardMarkup(
        keyboard, resize_keyboard=True, one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Выбери уровень игры: Простой/Сложный", reply_markup=markup_key,)
    return START


def start(update, context):
    case_lever.info = update.message.text
    if 'Простой' in case_lever.info or "Сложный" in case_lever.info:
        lever = str(
            f"{user_name}, твой ход! Введите кол-во конфет (от 1 до {max_candys_step}): ")
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=lever)
        return CANDY

    else:

        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Я тебя не понимаю")
        return START


def candy(update, context):
    global bank_candys, max_candys_step
    img_user_win = open('despicable-me-minions.mp4', 'rb')
    img_bot_win = open('terminator.mp4', 'rb')
    nope = open('terminator-nope.mp4', 'rb')
    user = update.message.from_user  # определяем пользователя

    stack_candy = bank_candys

    if update.message.text == '/stop':
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="До встречи! Захочешь поиграть - пиши!")
        context.bot.send_sticker(
            update.effective_chat.id, 'CAACAgIAAxkBAAEFokFjArLX1-q_1m2b_yazQSabI-X4LgACZwoAAu3PkUqxorJ-bFxV6SkE')    
        return ConversationHandler.END
    elif update.message.text.isdigit() == False:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Нужно ввести число! (выход по слову /stop)")
    else:
        step_game = int(update.message.text)

        if (step_game > max_candys_step) or (step_game == 0):
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Так нельзя!) Возьми от 1 до {max_candys_step} конфет! Попробуй еще раз!")
            context.bot.send_video(update.effective_chat.id, nope)
        # игрок забирает остатки конфет
        elif (step_game == stack_candy) and (step_game < (max_candys_step+1)):
            context.bot.send_video(update.effective_chat.id, img_user_win)
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=f"{user_name}, поздравляю! Ты выйграл(а)")
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Поиграем ещё? да/нет")
            return YESNO
        # ход бота и конфет 28 и меньше - тогда бот проиграл
        elif (stack_candy - step_game) < (max_candys_step+1):
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="ХА ХА ХА! Я забираю остаток конфет и я выиграл!")
            context.bot.send_video(update.effective_chat.id, img_bot_win)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Поиграем ещё раз? да/нет")
            return YESNO
        else:
            stack_candy = stack_candy - step_game

            if "Простой" in case_lever.info:
                step_bot = random.randint(1, max_candys_step+1)
            elif "Сложный" in case_lever.info:
                if stack_candy % (max_candys_step+1) == 0:
                    step_bot = max_candys_step
                else:
                    step_bot = stack_candy % (max_candys_step+1)

            # ход бота
            msg = f"Мой ход: {step_bot}. \n В куче осталось {(stack_candy - step_bot)}"
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=msg)
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=f.get_msg_bot())
            stack_candy -= step_bot  # определяем остаток конфет в куче
            bank_candys = stack_candy
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"{user_name}, {f.get_msg_for_user()} (выход по слову /stop)")


def end(update, context):
    user = update.message.from_user  # определяем пользователя
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Конец игры!")
    # Заканчиваем игру. Не работает.
    return ConversationHandler.END


candy_handler = ConversationHandler(
    entry_points=[CommandHandler('start', game)],
    states={
        USER: [MessageHandler(Filters.text, get_name)],
        YESNO: [MessageHandler(Filters.text, user_yes_no)],
        BANK: [MessageHandler(Filters.text, get_candys)],
        LEVEL: [MessageHandler(Filters.text, level)],
        START: [MessageHandler(Filters.text, start)],
        CANDY: [MessageHandler(Filters.text, candy)]
    },
    fallbacks=[CommandHandler('end', end)],
)


dispatcher.add_handler(candy_handler)


print('start bot')
updater.start_polling()
updater.idle()
