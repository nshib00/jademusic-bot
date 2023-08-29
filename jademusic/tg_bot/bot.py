import requests
import telebot
from os import getenv
from dotenv import load_dotenv
import logging

import keyboard
import tracks, albums, playlists
import info, user


logger = logging.getLogger(__name__)
log_format ='[%(levelname)s] %(asctime)s | %(module)s.%(funcName)s <line %(lineno)d> | %(message)s'
logging.basicConfig(format=log_format, level='WARNING', filename='../logs.log')

load_dotenv('C:/MyPrograms/JadeMusic/jademusic/jademusic/.env')
BOT_TOKEN = getenv('BOT_TOKEN')
ADMIN_CHAT_ID = getenv('ADMIN_CHAT_ID')
JADEMUSIC_HOST = getenv('JADEMUSIC_HOST')


bot = telebot.TeleBot(BOT_TOKEN)
logger.info('Bot started.')


class Pages:
    albums_page = 1
    playlists_page = 1


@bot.message_handler(commands=['start'])
def start_cmd_handler(message):
    welcome = '👋Привет! Я бот JadeMusic, с моей помощью можно с удобством скачивать треки, альбомы, плейлисты разных жанров без поиска подходящего сайта!'
    bot.send_message(message.chat.id, welcome)
    if not user.check_user_is_registered(message):
        user.register_user(message)
    #     authorize_user(user=make_user_dict(message))
    keyboard.make_start_buttons(bot, chat_id=message.chat.id)


@bot.message_handler(commands=['about'])
def about_cmd_handler(message):
    keyboard.show_back_button(bot, message, text=info.bot_info)



# def change_download_folder_path(msg):
#     paths.change_download_path(new_path=msg.text)
#     bot.send_message(msg.chat.id, f'Путь изменен успешно. Новый путь:\n{PathManager.download_path}')
#     keyboard.show_back_button(bot, msg)

@bot.callback_query_handler(func=lambda callback: callback.data == 'back')
def back_cb_handler(callback):
    keyboard.make_start_buttons(bot, chat_id=callback.message.chat.id)


@bot.callback_query_handler(func=lambda callback: callback.data == 'tracks_query')
def tracks_query_cb_handler(callback):
    tracks.get_tracks_by_query(bot, message=callback.message)


@bot.callback_query_handler(func=lambda callback: callback.data == 'tracks')
def tracks_cb_handler(callback):
    keyboard.show_tracks_keyboard(bot, message=callback.message)


@bot.callback_query_handler(func=lambda callback: callback.data == 'albums')
def albums_cb_handler(callback):
    albums.get_albums(bot, message=callback.message, get_to_download=False)
    keyboard.show_albums_menu_keyboard(bot, message=callback.message, albums_page=Pages.albums_page)


@bot.callback_query_handler(func=lambda callback: callback.data.startswith('tracks=page'))
def tracks_paginate_cb_handler(callback):
    if callback.data.endswith('prev'):
        tracks.TrackManager.page -= 1
    elif callback.data.endswith('next'):
        tracks.TrackManager.page += 1
    tracks.print_tracks(bot=bot, message=callback.message)


@bot.callback_query_handler(func=lambda callback: callback.data.startswith('albums=page'))
def albums_paginate_cb_handler(callback):
    if callback.data.endswith('prev'):
        Pages.albums_page -= 1
    elif callback.data.endswith('next'):
        Pages.albums_page += 1
    albums.get_albums(bot, message=callback.message, get_to_download=False, page=Pages.albums_page)
    keyboard.show_albums_menu_keyboard(bot, message=callback.message, albums_page=Pages.albums_page)


@bot.callback_query_handler(func=lambda callback: callback.data.startswith('download_tracks'))
def tracks_download_cb_handler(callback):
    keyboard.show_tracks_download_keyboard(bot, message=callback.message)


@bot.callback_query_handler(func=lambda callback: callback.data.startswith('download_album'))
def albums_download_cb_handler(callback):
    if 'page=' in callback.data:
        page = callback.data.split('=')[-1]
    else:
        page = 1
    albums.get_album_by_id(bot, callback.message, page=page)


@bot.callback_query_handler(func=lambda callback: callback.data == 'playlists')
def playlists_cb_handler(callback):
    playlists.get_playlists(bot, message=callback.message, get_to_download=False)
    keyboard.show_playlists_menu_keyboard(bot, message=callback.message, playlists_page=Pages.playlists_page)


@bot.callback_query_handler(func=lambda callback: callback.data.startswith('playlists=page'))
def playlists_paginate_cb_handler(callback):
    if callback.data.endswith('prev'):
        Pages.playlists_page -= 1
    elif callback.data.endswith('next'):
        Pages.playlists_page += 1
    playlists.get_playlists(bot, message=callback.message, get_to_download=False, page=Pages.playlists_page)
    keyboard.show_playlists_menu_keyboard(bot, message=callback.message, playlists_page=Pages.playlists_page)


@bot.callback_query_handler(func=lambda callback: callback.data.startswith('download_playlist'))
def playlist_download_cb_handler(callback):
    if 'page=' in callback.data:
        page = callback.data.split('=')[-1]
    else:
        page = 1
    playlists.get_playlist_by_id(bot, callback.message, page=page)


@bot.callback_query_handler(func=lambda callback: callback.data == 'popular_tracks')
def popular_tracks_cb_handler(callback):
    tracks.get_popular_tracks(bot, message=callback.message)


@bot.callback_query_handler(func=lambda callback: callback.data == 'new_tracks')
def new_tracks_cb_handler(callback):
    tracks.get_new_tracks(bot, message=callback.message)


@bot.callback_query_handler(func=lambda callback: callback.data == 'dmode=only_one')
def download_only_one_cb_handler(callback):
    tracks.download_tracks(bot, message=callback.message, download_mode='only_one')


@bot.callback_query_handler(func=lambda callback: callback.data == 'dmode=by_numbers')
def download_by_numbers_cb_handler(callback):
    tracks.download_tracks(bot, message=callback.message, download_mode='by_numbers')


@bot.callback_query_handler(func=lambda callback: callback.data == 'dmode=all')
def download_by_numbers_cb_handler(callback):
    tracks.download_tracks(bot, message=callback.message, download_mode='all')


@bot.callback_query_handler(func=lambda callback: callback.data == 'dmode=first_n')
def download_by_numbers_cb_handler(callback):
    tracks.download_tracks(bot, message=callback.message, download_mode='first_n')


@bot.callback_query_handler(func=lambda callback: callback.data == 'download_popular')
def download_popular_cb_handler(callback):
    tracks.download_popular_tracks(bot, callback.message)


@bot.callback_query_handler(func=lambda callback: callback.data == 'download_new')
def download_new_cb_handler(callback):
    tracks.download_new_tracks(bot, callback.message)

# @bot.callback_query_handler(func=lambda callback: callback.data)
# def check_callback_data(callback):
#     match callback.data:
        # case 'settings':
        #     keyboard.make_settings_buttons(bot, chat_id=callback.message.chat.id)
        # case 'change_folder':
        #     bot.send_message(callback.message.chat.id, f'Текущий путь папки для загрузки:\n{PathManager.download_path}')
        #     folder_query_msg = bot.reply_to(callback.message, 'Введите путь до нужной папки:')
        #     bot.register_next_step_handler(folder_query_msg, change_download_folder_path)


@bot.message_handler(func=lambda msg: msg.text.lower() in ('треки', 'альбомы', 'плейлисты'))
def start_buttons_reply(message):
    match message.text.lower():
        case 'треки':
            keyboard.show_tracks_keyboard(bot, message=message)
        case 'альбомы':
            keyboard.show_albums_keyboard(bot, chat_id=message.chat.id)
        case 'плейлисты':
            playlists.get_playlists(message=message)


@bot.message_handler(content_types=['text'])
def help_handler(message):
    cmd_list = '''
    Список команд бота:
/start - __открывает главное меню бота__
/about - __информация о боте__
'''
    bot.send_message(message.chat.id, cmd_list, parse_mode='markdown')


while True:
    try:
        bot.polling(logger_level=logging.INFO, skip_pending=True, restart_on_change=True)
    except requests.exceptions.ConnectionError as exc:
        error_text = f'Нет подключения к интернету.\n{exc.__class__.__name__}: {exc}.'
        logger.error(error_text)
        break
    except Exception as exc:
        error_text = f'Error occured. {exc.__class__.__name__}: {exc}.'
        logger.error(error_text)
        requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={ADMIN_CHAT_ID}&text={error_text}')
