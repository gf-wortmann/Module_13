from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


api = "__TOKEN__"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


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
kb.row(btn1, btn2)

kb2 = InlineKeyboardMarkup()
btn_2_1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
btn_2_2 = InlineKeyboardButton(text='Формулы расчета', callback_data='formulae')
kb2.add(btn_2_1)
kb2.add(btn_2_2)


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
    await state.get_data()
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await state.get_data()
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