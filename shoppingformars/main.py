from aiogram import Bot,Dispatcher,executor,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import logging

from state import *
from default_btn import *
from inlayn_btn import *
from database import DatabaseManager

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "6878062588:AAGqQVplR3FF2S4jt2q69bG79Wlwre0cAKk"

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot,storage=storage)


database = DatabaseManager("marshop.db")
async def on_startup(dp):
    await database.create_tables()
    await bot.send_message(chat_id=909437832,text="Bot has started")

async def on_shutdown(dp):
    await bot.send_message(chat_id=909437832,text="Bot has stopped")

@dp.message_handler(commands="start")
async def start_handler(message:types.Message):
    chat_id = message.chat.id
    user = await database.get_user_by_chat_id(chat_id=chat_id)
    if user:
        await message.answer(f"Welcome to mars shop bot dear {user[2]}",reply_markup=shop_menu)
    else:
        await message.answer("Welcome to mars shop")
        await message.answer("You can register for use this bot\nEnter full name: ")
        await RegisterState.full_name.set()

@dp.message_handler(commands="help")
async def start_handler(message:types.Message):
    await message.answer("Bu help buyrugi")


@dp.message_handler(state=RegisterState.full_name)
async def full_name_handler(message:types.Message,state:FSMContext):
    full_name = message.text
    await state.update_data(full_name=full_name)
    await message.answer("Share Contact",reply_markup=phone_number)
    await RegisterState.phone_number.set()

@dp.message_handler(state=RegisterState.phone_number,content_types=types.ContentType.CONTACT)
async def phone_number_handler(message:types.Message,state:FSMContext):
    phone_number = message.contact.phone_number
    await state.update_data(phone_number=phone_number)
    await state.update_data(chat_id=message.chat.id)
    data = await state.get_data()
    if await database.register_user(data=data):
        await message.answer("Successfully registreted and you can use bot",reply_markup=shop_menu)
    else:
        await message.answer("Register Error")
    await state.finish()
    
@dp.message_handler(text="My Products")
async def my_product_handler(message:types.Message):
    await message.answer("Choice Command",reply_markup=my_products)
    
@dp.message_handler(text="MARS Shop")
async def marsshop_hendler(message:types.Message):
    start = 0
    total = await database.get_product_count_by_status(True)
    total = total[0]
    end = 4 if total>4 else total
    products=await database.marsshop_prodacts(True,end,start)
    number_btns = await mars_shop_btn(end-start)
    print(products)
    text = f"""Natijalar {start+1}-{end} {total} dan\n"""
    for i,product in enumerate(products):
        text+=f"{i+1}. {product[1]}-{product[4]}\n"
    print(text)
    await message.answer(text,reply_markup=number_btns)
    
    # for product in products:
    #     await message.answer_photo(product[2],
    #     caption=f"Product ID {product[0]}\n:Name: {product[1]}\nPrice: {product[3]} so'm\nCount: {product[5]}\nDescription: {product[4]}",
    #     reply_markup=buy_product)

@dp.message_handler(text="🛒Show Products")
async def my_product_handler(message:types.Message):
    chat_id = message.chat.id
    products = await database.get_all_products_by_chat_id(chat_id=chat_id)
    for product in products:
        await message.answer_photo(product[2],
        caption=f"Product ID {product[0]}\n:Name: {product[1]}\nPrice: {product[3]} so'm\nCount: {product[5]}\nDescription: {product[4]}",
        reply_markup=show_prodact_btns(product[-1]))

@dp.callback_query_handler(text="ad_or_del_shop")
async def add_shop_handler(call:types.CallbackQuery):
    caption = call.message.caption
    line_id = caption.split('\n')[0]    
    id = line_id.split(" ")[-1]
    
    add_or_rem = call.message.reply_markup.inline_keyboard[-1][0].text
    if add_or_rem == "➖Remove to shop":
        if  await database.update_product_status(id,False):
            await call.message.edit_reply_markup(reply_markup=show_prodact_btns(False))
            await call.answer("Product is removed from MARSHOP ")
        else:
            await call.message.answer("Error Remove Product")
    else:
        if await database.update_product_status(id,True):
            await call.message.edit_reply_markup(reply_markup=show_prodact_btns(True))
            await call.answer("Product is added from MARSHOP ")
        else:
            await call.message.answer("Error Add Product")
    await call.answer()
    
@dp.message_handler(text="⬅️Back")
async def add_product_handler(message:types.Message):
    await message.answer("Main Menu",reply_markup=shop_menu)

@dp.message_handler(text="➕Add Product")
async def add_product_handler(message:types.Message):
    await message.answer("Enter product name: ")
    await AddProductState.name.set()
    
@dp.message_handler(state=AddProductState.name)
async def add_product_name_handler(message:types.Message,state:FSMContext):
    product_name = message.text
    await state.update_data(name=product_name)
    await message.answer("Send product photo: ")
    await AddProductState.photo.set()
    
@dp.message_handler(state=AddProductState.photo,content_types="photo")
async def add_product_name_handler(message:types.Message,state:FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    await message.answer("Enter product price: ")
    await AddProductState.price.set()

@dp.message_handler(state=AddProductState.price)
async def add_product_name_handler(message:types.Message,state:FSMContext):
    product_price = message.text
    await state.update_data(price=product_price)
    await message.answer("Enter product count: ")
    await AddProductState.count.set()

@dp.message_handler(state=AddProductState.count)
async def add_product_name_handler(message:types.Message,state:FSMContext):
    product_count = message.text
    await state.update_data(count=product_count)
    await message.answer("Enter product description: ")
    await AddProductState.description.set()
    
@dp.message_handler(state=AddProductState.description)
async def add_product_name_handler(message:types.Message,state:FSMContext):
    product_desc = message.text
    await state.update_data(description=product_desc)
    data = await state.get_data()
    chat_id = message.chat.id
    user = await database.get_user_by_chat_id(chat_id)
    print(user)
    data["user_id"] = user[0]
    await database.add_product(data)
    await message.answer("Successfully added")
    await state.finish() 
    
if __name__ == "__main__":
    executor.start_polling(dp,skip_updates=True,on_startup=on_startup,on_shutdown=on_shutdown)
