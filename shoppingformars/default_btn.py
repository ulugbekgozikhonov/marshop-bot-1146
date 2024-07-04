from aiogram.types import ReplyKeyboardMarkup,KeyboardButton


phone_number = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Share Contact",request_contact=True)
        ]
    ],resize_keyboard=True
)

shop_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("My Products"),
            KeyboardButton("MARS Shop"),
        ],
        [
            KeyboardButton("My Orders"),
            KeyboardButton("Profile"),
        ]
    ],resize_keyboard=True
)

my_products = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Show Products"),
            KeyboardButton("Add Product"),
        ]
    ],resize_keyboard=True
)