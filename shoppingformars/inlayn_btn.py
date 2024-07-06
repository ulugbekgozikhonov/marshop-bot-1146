from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

def show_prodact_btns(add_or_del_shop):

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                
                InlineKeyboardButton("Delete product",callback_data='del_prod'),
                InlineKeyboardButton("Edit product",callback_data='edit_prod')
            ],
            [
                InlineKeyboardButton(add_or_del_shop,callback_data='ad_or_del_shop')
            ]
        ]
    )

