from aiogram.dispatcher.filters.state import State,StatesGroup

class RegisterState(StatesGroup):
    full_name = State()
    phone_number = State()

class ProductState(StatesGroup):
    product = State()
    
class AddProductState(StatesGroup):
    name = State()
    photo = State()
    price = State()
    count = State()
    description = State()
    price = State()