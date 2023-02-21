import aiogram

def markup(sp_name):
    info_markup = aiogram.types.InlineKeyboardMarkup()
    for i in sp_name:
        info_markup.row(aiogram.types.InlineKeyboardButton(text=i, callback_data=i))
    # info_markup.row(aiogram.types.InlineKeyboardButton(text='📖Правила📖', url='https://t.me/joinchat/AAAAAFAOJoxviKZQ66quDw'))
    # info_markup.row(aiogram.types.InlineKeyboardButton(text='☎Контакты☎', callback_data='contacts'))

    return info_markup


