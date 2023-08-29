from telebot import types


def make_start_buttons(bot, chat_id):
    kb = types.InlineKeyboardMarkup(row_width=2, keyboard=[
        [types.InlineKeyboardButton(text='🎶Скачать треки', callback_data='tracks')],
        [
            types.InlineKeyboardButton(text='📀Скачать альбомы', callback_data='albums'),
            types.InlineKeyboardButton(text='🎵Скачать плейлисты', callback_data='playlists')
        ]
    ])
    # settings_btn = types.InlineKeyboardButton(text='Настройки бота', callback_data='settings')
    bot.send_message(chat_id, '🏠Главное меню JadeMusic.', reply_markup=kb)


def show_back_button(bot, message, text='Вернуться назад'):
    kb = types.InlineKeyboardMarkup(keyboard=[
        [types.InlineKeyboardButton(text='⬅️Назад', callback_data='back')]
    ])
    bot.send_message(message.chat.id, text, reply_markup=kb)


def show_tracks_keyboard(bot, message):
    kb = types.InlineKeyboardMarkup(keyboard=[
        [
            types.InlineKeyboardButton(text='⭐️Популярное⭐️', callback_data='popular_tracks'),
            types.InlineKeyboardButton(text='⚡️Новинки⚡️', callback_data='new_tracks'),
            types.InlineKeyboardButton(text='🔍По запросу🔎', callback_data='tracks_query'),
        ],
        [types.InlineKeyboardButton(text='⬅️Назад', callback_data='back')]
    ])
    msg_text = 'Если вы хотите найти треки по исполнителю, названию или ключевому слову, нажмите "По запросу".'
    bot.send_message(message.chat.id, msg_text, reply_markup=kb)


def show_artist_param_keyboard(bot, message):
    kb = types.InlineKeyboardMarkup(keyboard=[
        [
            types.InlineKeyboardButton(text='🧑‍🎤По исполнителю', callback_data='artist=1'),
            types.InlineKeyboardButton(text='🅰️По названию', callback_data='artist=0')
        ]
    ])
    bot.send_message(message.chat.id, 'Выберите режим поиска треков:', reply_markup=kb)


def show_tracks_menu_keyboard(bot, chat_id, tracks_page):
    msg = 'Можно продолжить поиск треков, скачать треки из списка или вернуться на главную страницу.'
    kb = make_pagination_keyboard(callback_data='tracks', page=tracks_page)
    kb.add(
        types.InlineKeyboardButton(text='🟢Скачать', callback_data=f'download_tracks=page-{tracks_page}'),
        types.InlineKeyboardButton(text='⬅️Назад', callback_data='back')
    )
    bot.send_message(chat_id, msg, reply_markup=kb)


def show_tracks_download_keyboard(bot, message):
    kb = types.InlineKeyboardMarkup(row_width=2, keyboard=[
        [
            types.InlineKeyboardButton(text='*️⃣Все', callback_data='dmode=all'),
            types.InlineKeyboardButton(text='🔣Первые несколько', callback_data='dmode=first_n')
        ],
        [
            types.InlineKeyboardButton(text='🔢По номерам', callback_data='dmode=by_numbers'),
            types.InlineKeyboardButton(text='1️⃣Только первый трек', callback_data='dmode=only_one')
        ],
        [types.InlineKeyboardButton(text='⬅️Назад', callback_data='back')]
    ])
    msg_text = 'Выберите режим, в котором хотели бы скачать найденные треки.'
    bot.send_message(message.chat.id, msg_text, reply_markup=kb)


def show_popular_tracks_download_keyboard(message, bot):
    kb = types.InlineKeyboardMarkup(keyboard=[
        [types.InlineKeyboardButton(text='🟢Скачать', callback_data='download_popular')],
        [types.InlineKeyboardButton(text='⬅️Назад', callback_data='back')]
    ])
    msg_text = 'Нажмите кнопку "Скачать", чтобы начать загрузку треков.'
    bot.send_message(message.chat.id, msg_text, reply_markup=kb)


def show_new_tracks_download_keyboard(message, bot):
    kb = types.InlineKeyboardMarkup(keyboard=[
        [types.InlineKeyboardButton(text='🟢Скачать', callback_data='download_new')],
        [types.InlineKeyboardButton(text='⬅️Назад', callback_data='back')]
    ])
    msg_text = 'Нажмите кнопку "Скачать", чтобы начать загрузку треков.'
    bot.send_message(message.chat.id, msg_text, reply_markup=kb)


def show_first_n_dmode_btn(bot, message):
    kb = types.InlineKeyboardMarkup(keyboard=[
        [types.InlineKeyboardButton(text='Первые несколько', callback_data='dmode=first_n')],
        [types.InlineKeyboardButton(text='⬅️Назад', callback_data='back')]
    ])
    msg_text = 'Нажмите на кнопку и затем укажите целое число, большее 1.'
    bot.send_message(message.chat.id, msg_text, reply_markup=kb)


def show_by_numbers_dmode_btn(bot, message):
    kb = types.InlineKeyboardMarkup(keyboard=[
        [types.InlineKeyboardButton(text='По номерам', callback_data='dmode=by_numbers')],
        [types.InlineKeyboardButton(text='⬅️Назад', callback_data='back')]
    ])
    msg_text = 'Нажмите на кнопку "По номерам" и затем укажите целое число, большее 1.'
    bot.send_message(message.chat.id, msg_text, reply_markup=kb)


def make_pagination_keyboard(callback_data: str, page:int=1) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup()
    if page == 1:
        kb.add(
            types.InlineKeyboardButton(text='🔍Найти еще', callback_data=f'{callback_data}=page-next')
        )
    elif page > 1:
        kb.add(
            types.InlineKeyboardButton(text='◀️Предыдущая страница', callback_data=f'{callback_data}=page-prev'),
            types.InlineKeyboardButton(text='▶️Следующая страница', callback_data=f'{callback_data}=page-next'),
        )
    else:
        raise ValueError(f'Ошибка пагинации: номер страницы не может быть меньше 1. Значение номера: {page}.')
    return kb


def show_albums_keyboard(bot, chat_id):
    msg = '''
       Если вы хотите найти альбом по названию или исполнителю, введите запрос. 
       Если хотите выбрать жанр, нажмите на кнопку.
       '''
    kb = types.InlineKeyboardMarkup(keyboard=[
        [
            types.InlineKeyboardButton(text='🔶Альбомы по жанрам', callback_data='album_genres'),
            types.InlineKeyboardButton(text='🔠Альбомы по запросу', callback_data='albums_query')
        ],
        [types.InlineKeyboardButton(text='⬅️Назад', callback_data='back')]
    ])
    bot.send_message(chat_id, msg, reply_markup=kb)


def show_albums_menu_keyboard(bot, message, albums_page):
    kb = make_pagination_keyboard(callback_data='albums', page=albums_page)
    kb.add(
        types.InlineKeyboardButton(text='🟢Скачать', callback_data=f'download_album-page={albums_page}'),
        types.InlineKeyboardButton(text='⬅️Назад', callback_data='back')
    )
    msg = 'Можно продолжить поиск альбомов, скачать один из найденных или вернуться на главную страницу.'
    bot.send_message(message.chat.id, msg, reply_markup=kb)
    return kb


def show_playlists_keyboard(bot, message):
    kb = types.InlineKeyboardMarkup(keyboard=[
        [types.InlineKeyboardButton(text='🟢Скачать плейлисты', callback_data='playlists')],
        [types.InlineKeyboardButton(text='⬅️Назад', callback_data='back')]
    ])
    bot.send_message(message.chat.id, 'Раздел "Плейлисты".', reply_markup=kb)


def show_playlists_menu_keyboard(bot, message, playlists_page):
    kb = make_pagination_keyboard(callback_data='playlists', page=playlists_page)
    kb.add(
        types.InlineKeyboardButton(text='🟢Скачать', callback_data=f'download_playlist-page={playlists_page}'),
        types.InlineKeyboardButton(text='⬅️Назад', callback_data='back')
    )
    msg = 'Можно продолжить поиск плейлистов, скачать один из найденных или вернуться на главную страницу.'
    bot.send_message(message.chat.id, msg, reply_markup=kb)
    return kb


# def make_settings_buttons(bot, chat_id):
#     kb = types.InlineKeyboardMarkup()
#     change_folder_path_btn = types.InlineKeyboardButton(text='🗂Сменить папку для загрузки', callback_data='change_folder')
#     back_btn = types.InlineKeyboardButton(text='⬅️Назад', callback_data='back')
#     keyboard.add(change_folder_path_btn, back_btn)
#     bot.send_message(chat_id, '⚙️Настройки JadeMusic.⚙️', reply_markup=kb)