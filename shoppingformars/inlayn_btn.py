from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

def show_prodact_btns(status):

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                
                InlineKeyboardButton("❌Delete product",callback_data='del_prod'),
                InlineKeyboardButton("🔍Edit product",callback_data='edit_prod')
            ],
            [
                InlineKeyboardButton("➖Remove to shop" if status else "➕Add to shop",callback_data='ad_or_del_shop')
            ]
        ]
    )
    
buy_product = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Buy Product",callback_data="buy_prod")
        ]
    ]
)


async def mars_shop_btn(count):
    mars_shop = InlineKeyboardMarkup(row_width=3)
    
    for i in range(count):
        btn = InlineKeyboardButton(f"{i+1}",callback_data=f"btn_{i+1}")
        if i % 2 == 0:
            mars_shop.add(btn)
        else:
            mars_shop.insert(btn)
            
    return mars_shop.add(InlineKeyboardButton("⬅️",callback_data="orqaga"),
                         InlineKeyboardButton("❌",callback_data="yopish"),
                         InlineKeyboardButton("➡️",callback_data="oldinga"))