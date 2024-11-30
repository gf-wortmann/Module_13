from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import crud_functions as cruds

api = "__API_TOKEN__"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
contain = cruds.get_all_products()


class UserState(StatesGroup):
    address = State()
    age = State()
    growth = State()
    weight = State()


def mifflin_st_jeor(data):
    user_weight = float(data['weight'])
    user_growth = float(data['growth'])
    user_age = int(data['age'])
    calories = 10 * user_weight + 6.25 * user_growth - 5 * user_age + 5
    return calories


kb = ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = KeyboardButton(text='Информация')
btn2 = KeyboardButton(text='Рассчитать')
btn3 = KeyboardButton(text='Купить')
kb.row(btn1, btn2)
kb.row(btn3)

kb2 = InlineKeyboardMarkup()
btn_2_1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
btn_2_2 = InlineKeyboardButton(text='Формулы расчета', callback_data='formulae')
kb2.add(btn_2_1)
kb2.add(btn_2_2)

kb_buying_list = InlineKeyboardMarkup()
btn_bl_1 = InlineKeyboardButton(text=contain[0][1], callback_data='product_buying')
btn_bl_2 = InlineKeyboardButton(text=contain[1][1], callback_data='product_buying')
btn_bl_3 = InlineKeyboardButton(text=contain[2][1], callback_data='product_buying')
btn_bl_4 = InlineKeyboardButton(text=contain[3][1], callback_data='product_buying')
kb_buying_list.row(btn_bl_1, btn_bl_2, btn_bl_3, btn_bl_4)


@dp.message_handler(text=btn3.text)
async def get_buying_list(message):
    for i in range(1, 4 + 1):
        with open(f'../../img/{i}.webp', "rb") as img:
            await message.answer(
                f"Название: {contain[i - 1][1]} | Описание: {contain[i - 1][2]} | Price: {contain[i - 1][3]}")
            await message.answer_photo(img)
    
    await message.answer("Выберите продукт для покупки:", reply_markup=kb_buying_list)


@dp.callback_query_handler(lambda call: call.data == 'product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@dp.message_handler(text=btn2.text)
async def main_menu(message):
    await message.answer("Выберите опцию:", reply_markup=kb2)


@dp.callback_query_handler(lambda call: call.data == 'calories')
async def inline_calculate(call):
    await set_age(call.message)
    await call.answer()


@dp.callback_query_handler(lambda call: call.data == 'formulae')
async def chow_formulae(call):
    await call.message.answer('calories = 10 * user_weight + 6.25 * user_growth - 5 * user_age + 5')
    await call.answer()


@dp.message_handler(text=btn1.text)
async def inform(message):
    await message.answer('Бот для расчета суточной нормы калорийности питания')


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer("Привет! Я - бот, помогающий Вашему здоровью.", reply_markup=kb)


@dp.message_handler(text=['calories'])
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    data = await state.get_data()
    await message.answer('Введите свой вес в кг:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    await state.finish()
    calories = mifflin_st_jeor(data)
    await message.answer(f"Суточная норма калорий равна {calories} ккал", reply_markup=kb)


@dp.message_handler()
async def all_message(message):
    print("Введите команду /start, чтобы начать общение.")
    await message.answer(message.text)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)