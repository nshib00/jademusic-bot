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


def get_albums(bot, message, page=1, get_to_download=False, print_albums=True) -> list[dict] | None:
    ''' Execute album/get API method. '''
    url = f'{API_URL}/album/get?page={page}'
    if print_albums:
        bot.send_message(message.chat.id, 'Ищу альбомы...')

    resp_json = musobj.get_response_json(url)
    albums = resp_json['data']['albums']
    albums_string = musobj.make_musobj_str(musobjs=albums)

    if not get_to_download and print_albums:
        musobj.print_musobjs(bot, message, albums, albums_string)
    return albums


def download_album(message, bot, albums, page=1) -> None:
    ''' Execute album/download API method. '''
    album_id = int(message.text) - 1
    album = albums[album_id]

    bot.send_message(message.chat.id, f'Скачиваю альбом "{album["title"]}"...')
    url = f'{API_URL}/album/download?page={page}&album_id={album_id+1}'
    session = HTMLSession()
    response = session.get(url)
    msg = utils.make_response_message(response, logger, downloading_object_title=album['title'], mode='album')
    keyboard.show_back_button(bot, message, msg)


def get_album_by_id(bot, message, page=1):
    albums = get_albums(bot, message, page=page, print_albums=False)
    album_id_message = bot.reply_to(message, 'Чтобы скачать конкретный альбом из списка, введите его номер.')
    bot.register_next_step_handler(album_id_message, download_album, bot=bot, albums=albums, page=page)
