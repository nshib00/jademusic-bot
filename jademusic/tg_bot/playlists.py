from dotenv import load_dotenv
from os import getenv
from requests_html import HTMLSession
import logging

import keyboard, utils, musobj

load_dotenv('C:/MyPrograms/JadeMusic/jademusic/jademusic/.env')
HOST = getenv('JADEMUSIC_HOST')
API_URL = HOST + '/' + getenv('API_URL')

logger = logging.getLogger(__name__)
log_format ='[%(levelname)s] %(asctime)s | %(module)s.%(funcName)s <line %(lineno)d> | %(message)s'
logging.basicConfig(format=log_format, level='WARNING', filename='../logs.log')


def get_playlists(bot, message, page=1, get_to_download=False, print_playlists=True) -> list[dict] | None:
    ''' Execute playlist/get API method. '''
    url = f'{API_URL}/playlist/get?page={page}'
    if print_playlists:
        bot.send_message(message.chat.id, 'Ищу плейлисты...')

    resp_json = musobj.get_response_json(url)
    playlists = resp_json['data']['playlists']
    playlists_string = musobj.make_musobj_str(musobjs=playlists)

    if not get_to_download and print_playlists:
        musobj.print_musobjs(bot, message, playlists, playlists_string)
    return playlists


def download_playlist(message, bot, playlists, page=1) -> None:
    ''' Execute playlist/download API method. '''
    playlist_id = int(message.text) - 1
    playlist = playlists[playlist_id]

    bot.send_message(message.chat.id, f'Скачиваю плейлист "{playlist["title"]}"...')
    url = f'{API_URL}/playlist/download?playlist_id={playlist_id+1}&page={page}'
    session = HTMLSession()
    response = session.get(url)
    msg = utils.make_response_message(response, logger, downloading_object_title=playlist['title'], mode='playlist')
    keyboard.show_back_button(bot, message, msg)


def get_playlist_by_id(bot, message, page=1):
    playlists = get_playlists(bot, message, page=page, print_playlists=False)
    playlist_id_message = bot.reply_to(message, 'Чтобы скачать конкретный плейлист, введите его номер.')
    bot.register_next_step_handler(playlist_id_message, download_playlist, bot=bot, playlists=playlists, page=page)
