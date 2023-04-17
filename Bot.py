import Parser #сам парсер
from config import TOKEN #Токен бота
import debug #Для вывода в консоль запросов пользователей

from aiogram import Bot, types #библиотеки для бота
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start():

    bot = Bot(token=TOKEN) #инициализируем объекты бота и диспетчера
    dp = Dispatcher(bot)

    #################################################################################
    inline_btn_1 = InlineKeyboardButton('Помощь', callback_data='button1_help')
    inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
    #ИНЛАЙН КНОПКА в меню /start
    @dp.callback_query_handler(lambda c: c.data == 'button1_help')
    async def process_callback_button1_help(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, 'Напиши мне название лекарства, а я его ,так уж и быть, поищу.\nДля этого нужно написать название желаемого лекарства и отправить его сообщением.')
    #################################################################################

    #################################################################################
    inline_btn_2 = InlineKeyboardButton('Вернуться обратно', callback_data='button2_return')
    inline_kb2 = InlineKeyboardMarkup().add(inline_btn_2)
    #ИНЛАЙН КНОПКА после поиска
    @dp.callback_query_handler(lambda c: c.data == 'button2_return')
    async def process_callback_button1_help(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id,"Привет!\nНапиши мне название лекарства, которое мы будем искать.", reply_markup=inline_kb1)
    #################################################################################

    #/START
    @dp.message_handler(commands=['start']) #Даём ответ на /start
    async def process_start_command(msg: types.Message):
        #kb = [
            #[types.KeyboardButton(text="Ибупрофен")],
            #[types.KeyboardButton(text="Нурофен")],
            #[types.KeyboardButton(text="Доктор мом")]
        #]
        #keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
        await msg.reply("Привет!\nНапиши мне название лекарства, которое мы будем искать.", reply_markup=inline_kb1)#reply_markup=(keyboard))

    #/HELP
    @dp.message_handler(commands=['help']) #Даём ответ на /help
    async def process_help_command(msg: types.Message):
        await msg.reply('Напиши мне название лекарства, а я его ,так уж и быть, поищу.\nДля этого нужно написать название желаемого лекарства и отправить его сообщением.')

    #ПРОСТО СООБЩЕНИЕ
    @dp.message_handler() #Даём ответ на простое сообщение (запрос на поиск лекарства)
    async def process_medkit_search(msg: types.Message):
        print(debug.current_datetime, msg.from_user.username, '=', msg.text) #Вывод в консоль всех запросов всех пользователей

        await msg.reply('Произвожу поиск по запросу "'+msg.text+'".')
        Parser.poisk = msg.text
        Parser.parse()
        await bot.send_message(msg.from_user.id, Parser.msg1, reply_markup=inline_kb2)

    executor.start_polling(dp) #Постоянное ожидание обновлений

